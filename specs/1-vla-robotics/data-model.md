# Content Structure Model: Vision-Language-Action Module

## Chapter Entities

### VoiceToActionChapter
- **title**: String (e.g., "Voice-to-Action with Whisper")
- **description**: String (overview of voice-to-action systems)
- **learning_objectives**: Array<String> (what students will learn)
- **sections**: Array<Section> (organized content sections)
- **examples**: Array<Example> (hands-on exercises)
- **frontmatter**: Object (Docusaurus metadata)

### CognitivePlanningChapter
- **title**: String (e.g., "Cognitive Planning with LLMs")
- **description**: String (overview of LLM-based planning)
- **learning_objectives**: Array<String> (what students will learn)
- **sections**: Array<Section> (organized content sections)
- **examples**: Array<Example> (hands-on exercises)
- **frontmatter**: Object (Docusaurus metadata)

### VisionManipulationChapter
- **title**: String (e.g., "Vision-Guided Manipulation")
- **description**: String (overview of vision-action integration)
- **learning_objectives**: Array<String> (what students will learn)
- **sections**: Array<Section> (organized content sections)
- **examples**: Array<Example> (hands-on exercises)
- **frontmatter**: Object (Docusaurus metadata)

## Content Section Entity
- **section_title**: String (title of the section)
- **content_type**: Enum ("concept", "example", "hands-on", "summary")
- **body**: String (main content in Markdown)
- **prerequisites**: Array<String> (what students need to know)
- **duration_minutes**: Integer (estimated time to complete)

## Example Entity
- **title**: String (descriptive title of the example)
- **description**: String (what the example demonstrates)
- **code_snippet**: String (executable code)
- **expected_output**: String (what students should see)
- **difficulty_level**: Enum ("beginner", "intermediate", "advanced")
- **estimated_time**: Integer (minutes to complete)

## Validation Rules
- All chapter titles must be unique within the module
- Learning objectives must align with functional requirements from spec
- All code examples must be syntactically valid and executable
- Frontmatter must conform to Docusaurus standards
- All content must target students with ROS 2, perception, and Python basics

## State Transitions
- Content progresses from speech recognition to cognitive planning to vision-action integration
- Each chapter builds upon previous knowledge
- Hands-on examples validate understanding of concepts
- Navigation structure guides students through learning progression