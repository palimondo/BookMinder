# BookMind: Apple Book Knowledge Extractor v1.0

## Background

This project stems from a desire to enhance my intellectual workflow through AI-assisted tools. With 25+ years of programming experience across multiple languages (JavaScript, Java, Scala, Swift, Python), I'm exploring ways to better leverage my reading and learning activities.

My information consumption primarily consists of:
1. **Audiobooks through Audible** - Often purchasing e-book versions to highlight important passages
2. **E-books with highlights** - Reading books and marking key passages with different colors
3. **Podcasts and video content** - Taking screenshot notes with timestamps from interviews with AI researchers and political content

I'm interested in the concept of a "second brain" but haven't fully committed to platforms like Obsidian, preferring DayOne for journaling. I've experimented with transcribing videos using TTS systems and various AI models.

My longer-term vision includes:
- Having meaningful conversations with AI about books I've read, as a form of active learning
- Creating a personalized programming assistant that understands TDD/BDD principles from my programming books
- Building custom MCP (Model Context Protocol) tools to enhance AI interactions

This project serves as both a practical tool for my knowledge workflow and an evaluation of Claude Code's capabilities as a potential pair programming partner for TDD/BDD development.

The project should be managed using a local `git` repository for version tracking, with the possibility of publishing it as an open-source project on GitHub in the future.

### 1. Project Overview

**Purpose:** Create a tool that extracts both full text and highlights from Apple Books, converting them to a structured format (primarily Markdown) for further analysis with LLMs and potential integration with knowledge management systems.

**End Goal:** Enable rich conversations with LLMs about book content by providing them with complete text sections, chapters, and highlighted passages with their context, supporting active learning and deeper exploration of concepts across reading materials.

### 2. Requirements

#### 2.1 Discovery Phase
- **Database Exploration**: Claude Code should thoroughly explore the file system to locate relevant documents and databases where Apple Books stores information about books, highlights, and notes
  - Search for SQLite databases and other data stores in Library folders
  - Examine common locations for application data storage
  - Document all discovered resources that might be relevant
- **Known Resources**:
  - `Books.plist` in `/Users/palimondo/Library/Containers/com.apple.BKAgentService/Data/Documents/iBooks/Books/`
  - EPUB files in the same directory
- **Test Case**:
  - "Growing Object-Oriented Software, Guided by Tests" (non-DRM):
    - Located at: `/Users/palimondo/Library/Containers/com.apple.BKAgentService/Data/Documents/iBooks/Books/401429854.epub`
- **Research**: Investigate online resources about Apple Books data storage if necessary
- Document all findings for future development phases

#### 2.2 EPUB Processing
- Develop functions to extract content from EPUB files
- Focus on correctly mapping highlight metadata to the actual text in EPUBs
- Handle different chapter file structures (e.g., `/OEBPS/html/ch05.html` in the test book)
- Extract surrounding paragraphs to provide context for highlighted passages

#### 2.3 Content Extraction
- **Progressive Content Extraction**:
  1. Extract complete chapters from EPUB files using table of contents data
  2. Extract sections and subsections within chapters
  3. Extract specific passages based on highlight metadata
- **Investigative Approach**:
  - Explore how highlights are stored (XPath locators? Text excerpts?)
  - Determine the mapping between highlight metadata and document content
  - Develop strategies for locating highlighted content within the full text
- Extract metadata including:
  - Highlight colors
  - Timestamp information
  - Chapter/section information
  - Book metadata (title, author, publication date)

#### 2.4 Output Format
- Create Markdown files that include:
  - Book metadata (title, author)
  - Highlight information (timestamp, color)
  - Highlighted text with surrounding context
- The exact format should be determined during development based on exploration findings
- Focus on creating a format that is both human-readable and optimized for LLM consumption

#### 2.5 Testing Strategy
- Implement test-driven development (TDD) for the tool itself
- Create unit tests for each component
- Develop integration tests that verify correct extraction and formatting
- Use specific highlights from test books as validation cases

#### 2.6 Interface
- Create a simple command-line interface for the proof-of-concept
- Focus on a single book initially with plans for future expansion

#### 2.7 DRM Handling
- Initially focus on non-DRM protected books like "Growing Object-Oriented Software"
- Document any DRM protection discovered during exploration (as found in "The Beginning of Infinity")
- Research potential approaches for accessing content in DRM-protected books as a secondary goal

### 3. Development Approach (TDD-Oriented)

#### Iterative Development Cycle
Instead of rigid phases, we'll take a test-driven approach with small, iterative cycles:

1. **Write a failing test** for the specific functionality needed
2. **Implement the minimal code** to pass the test
3. **Refactor** the implementation while keeping tests passing
4. **Repeat** with the next small piece of functionality

#### Key Iterations (Initial Plan)

1. **Database and Resource Discovery**
   - Test: Can we locate the databases and files where Apple Books stores book information and highlights?
   - Implementation: Code to scan the filesystem for relevant Apple Books data files

2. **Chapter Extraction**
   - Test: Can we extract a complete chapter from an EPUB file?
   - Test Case: Extract chapter 5 from "Growing Object-Oriented Software"
   - Implementation: Code to parse EPUB structure and extract chapter content

3. **Section and Subsection Extraction**
   - Test: Can we extract specific sections from within a chapter?
   - Test Case: Extract a specific section from chapter 5
   - Implementation: Logic to parse document structure and extract sections

4. **Highlight Metadata Understanding**
   - Test: Can we locate and parse the highlight metadata?
   - Test Case: Find metadata for yellow highlight "Start Each Feature with an Acceptance Test" from March 23, 2025
   - Implementation: Code to read and parse highlight metadata

5. **Highlight Locating**
   - Test: Can we match a highlight metadata entry to the actual text in the EPUB?
   - Test Case: Correctly identify the text "In many organizations" highlighted on July 14, 2024
   - Implementation: Functions to connect highlights with their source text

6. **Context Extraction**
   - Test: Can we extract the surrounding context of a highlighted passage?
   - Test Case: Extract paragraph context around the highlighted text
   - Implementation: Logic to determine paragraph boundaries and extract relevant context

7. **Content Formatting**
   - Test: Can we format extracted content as a clean Markdown file?
   - Test Case: Generate properly formatted Markdown for a chapter and its highlights
   - Implementation: Export functionality for chapters and highlights

Each iteration will be a complete cycle of red (failing test), green (passing implementation), and refactor phases, following TDD principles.

### 4. Implementation Considerations

#### Technical Stack
- **Language**: Python (chosen for its rich library ecosystem for data processing and EPUB handling)
- **EPUB Handling**: Use established libraries rather than custom parsers (e.g., `ebooklib`, `beautifulsoup4`)
- **Data Format**: Markdown with YAML frontmatter for maximum flexibility and readability



#### Error Handling
- Implement robust error handling for cases where:
  - Highlight metadata doesn't match EPUB content
  - EPUB content is inaccessible due to DRM
  - File structure varies between different books

#### Privacy & Implementation
- All processing happens locally on the machine
- No data sent to external services
- Implementation should be transparent and auditable

#### Future Extensibility
- The code structure should allow for easy addition of:
  - Support for more book formats (PDF, etc.)
  - Integration with tools like DayOne or LLM platforms
  - Batch processing of multiple books
  - Semantic analysis of highlights

### 5. First Tasks for Claude Code

1. **Filesystem Exploration**: Thoroughly search for Apple Books data
   - Search all Library folders for databases and config files related to Apple Books
   - Look for SQLite databases, property lists, and other data stores
   - Document all discovered resources with their paths and formats
   - Examine the content of Books.plist to understand its structure
   - Look specifically for highlight and annotation data

2. **EPUB Analysis**: Understand the structure of EPUB files
   - Examine the non-DRM test book structure (`401429854.epub`)
   - Parse the table of contents (toc.ncx) to understand chapter organization
   - Identify how chapter content is stored and accessed
   - Document the EPUB structure and content access approach

3. **Content Extraction Proof-of-Concept**: Extract a chapter
   - Extract a complete chapter from the test book
   - Preserve formatting and structure where possible
   - Format the extracted content as clean Markdown
   - Document the process and any challenges encountered

4. **Highlight Investigation**: Research highlight storage
   - Determine how Apple Books stores highlight information
   - Investigate the relationship between highlights and EPUB content
   - Develop a strategy for mapping highlights to content
   - Document findings and potential approaches

### 6. Success Criteria for Initial Proof-of-Concept

1. Successfully extract at least one highlight from the non-DRM test book
2. Correctly identify the highlight color and timestamp
3. Include sufficient context around the highlight for meaningful LLM interaction
4. Generate a clean, well-structured Markdown output
5. Document the process and findings to enable future expansion

### 7. Future Possibilities (Beyond Proof-of-Concept)

While focusing on a minimal viable implementation first, these ideas could be explored in future iterations:

1. **LLM Integration**
   - Direct integration with local LLMs via LM Studio
   - Custom MCP tools for discussing book content with Claude
   - Active learning conversations about book chapters

2. **Knowledge Graph**
   - Connecting concepts across different books
   - Identifying relationships between highlighted passages
   - Building a personal knowledge network similar to Obsidian's approach

3. **Multimedia Integration**
   - Connecting book highlights with related podcast notes
   - Linking audiobook timestamps to text highlights
   - Creating a unified knowledge repository across media types

4. **Learning Enhancement**
   - Spaced repetition system for reviewing important highlights
   - Automated quizzes generated from highlighted content
   - Synthesis of ideas across different books on similar topics

These possibilities represent potential directions rather than immediate requirements.
