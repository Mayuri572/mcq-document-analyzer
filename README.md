# MCQ Document Analyzer

An AI-powered document analysis system that extracts Multiple Choice Questions (MCQs) from images and PDF documents and converts them into structured JSON data.

## Project Overview

The system is designed to process question papers containing MCQs and automatically extract:

* Question number
* Question text
* Answer options
* Document/page information
* Question ordering and layout information

The system also handles documents with **two-column layouts**, ensuring that questions are reconstructed in the correct reading order.

## Key Features

* Image and PDF input
* OCR-based text extraction
* Two-column layout detection
* Correct reading-order reconstruction
* MCQ and option detection
* Structured JSON output
* Topic-wise question analysis
* Image preprocessing for better OCR accuracy
* Scalable processing architecture
* Algorithm and time-complexity analysis

## Processing Pipeline

```text
Image / PDF
     ↓
Document Preprocessing
     ↓
Layout Detection
     ↓
OCR
     ↓
Reading Order Reconstruction
     ↓
MCQ Extraction
     ↓
Topic Classification
     ↓
Structured JSON
```

## Example Output

```json
{
  "question_number": 1,
  "question": "What is the time complexity of binary search?",
  "options": [
    "O(n)",
    "O(log n)",
    "O(n log n)",
    "O(1)"
  ],
  "topic": "Algorithms"
}
```

## Current Scope

The initial implementation focuses on **English MCQ documents** in image and PDF formats, with support for both single-column and two-column layouts.

The architecture is designed to be extended to multilingual documents and more complex question-paper formats.

## Technology Stack

* Python
* OCR Engine
* OpenCV
* PDF Processing
* JSON
* Layout Analysis
* Natural Language Processing

## Project Goals

The main objective is to build a reliable and scalable pipeline for converting unstructured question-paper documents into structured, machine-readable MCQ data.

Detailed documentation will cover:

* Algorithm selection
* OCR and layout-analysis approaches
* Comparison of alternative tools
* Best-case and worst-case time complexity
* Accuracy considerations
* Processing strategy for large-scale document uploads
* Scalability for high-volume document processing

