def format_tool_name(name):
  if name == "Bash" then "Bash"
  elif name == "Read" then "Read"
  else name
  end;

def format_tool_input(input):
  if input.command? then input.command
  elif input.file_path? then input.file_path
  elif input.path? then input.path
  elif input.pattern? then input.pattern
  else tostring
  end;

. as $line
| if $line.type == "user" and ($line.message.content | type) == "string" then
    if $line.message.content | contains("<command-name>") and ($line.message.content | contains("<command-message>")) then
        # Extract command message (e.g., "expert-council is running…")
        "> /" + ($line.message.content | capture("<command-message>(?<msg>[^<]+)</command-message>") | .msg) + "\n"
    elif $line.message.content | startswith("<command-message>") then
        # Skip pure command-message entries without command-name
        empty
    else
        "> \(.message.content)\n"
    end
elif $line.type == "user" and ($line.message.content | type) == "array" and ($line.message.content[0].type == "text") and ($line.message.content[0].text | contains("[Request interrupted by user")) then
    # Handle interrupted requests that come as user text messages
    empty  # Skip the "[Request interrupted by user]" message itself
elif $line.type == "assistant" and ($line.message.content | type) == "array" and $line.message.content[0].type == "text" then
    "⏺ \($line.message.content[0].text)\n\n"
elif $line.type == "assistant" and ($line.message.content | type) == "array" and $line.message.content[0].type == "tool_use" then
    if $line.message.content[0].name == "TodoWrite" then
        "⏺ Update Todos"
    elif $line.message.content[0].name == "TodoRead" then
        "⏺ Read Todos"
    else
        "⏺ \(format_tool_name($line.message.content[0].name))(\(format_tool_input($line.message.content[0].input)))"
    end + "\n"
elif $line.type == "user" and ($line.message.content | type) == "array" and $line.message.content[0].type == "tool_result" then
    def format_output(text):
        text | split("\n") as $lines |
        if ($lines | length) > 3 then
            ($lines[0:3] | join("\n")) + "\n     … +" + ($lines | length | tostring) + " lines (ctrl+r to expand)"
        else
            text
        end;
    
    def format_todo_item(todo):
        def priority_map(p):
            if p == "high" then "P0"
            elif p == "medium" then "P1"
            elif p == "low" then "P2"
            else "P?"
            end;
        
        def status_symbol(s):
            if s == "completed" then "☒"
            elif s == "in_progress" then "◐"
            else "☐"
            end;
        
        "\(status_symbol(todo.status)) \(todo.content) (\(priority_map(todo.priority)))";
    
    if ($line.toolUseResult? and ($line.toolUseResult | type) == "object" and $line.toolUseResult.newTodos?) then
        # TodoWrite result
        "\n  ⎿  " + ($line.toolUseResult.newTodos | map(format_todo_item(.)) | join("\n     ")) + "\n"
    elif ($line.toolUseResult? and ($line.toolUseResult | type) == "array") then
        # TodoRead result - toolUseResult is an array of todos
        "\n  ⎿  " + ($line.toolUseResult | map(format_todo_item(.)) | join("\n     ")) + "\n"
    else
        # Regular tool result
        # Check if this is an interrupted request
        if ($line.message.content[0].content | contains("[Request interrupted by user")) then
            "  ⎿  Interrupted by user\n\n  ⎿  Interrupted by user\n"
        else
            # Regular tool result
            "  ⎿  Waiting…\n\n  ⎿  " + 
            (if $line.toolUseResult? then
                if $line.toolUseResult | type == "string" then
                    format_output($line.toolUseResult)
                elif ($line.toolUseResult | type == "object") and ($line.toolUseResult.stdout?) and ($line.toolUseResult.stdout != "") then
                    format_output($line.toolUseResult.stdout)
                else
                    format_output($line.message.content[0].content | tostring)
                end
            else
                format_output($line.message.content[0].content | tostring)
            end) + "\n"
        end
    end
else
    empty
end