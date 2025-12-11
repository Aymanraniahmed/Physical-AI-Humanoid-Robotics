# Physical AI Humanoid Robotics: A Technical Guide

A comprehensive, beginner-friendly technical book covering Physical AI and humanoid robotics, from foundational concepts through advanced Vision-Language-Action (VLA) systems.

## Overview

This book guides readers through:
- **Physical AI Fundamentals**: Embodied intelligence, sensors, actuators, and digital twins
- **Module 1: ROS 2** - The robotic nervous system (nodes, topics, services, URDF)
- **Module 2: Simulation** - Digital twins with Gazebo and Unity
- **Module 3: NVIDIA Isaac** - GPU-accelerated perception and navigation
- **Module 4: VLA Systems** - Voice-Language-Action integration with LLMs
- **Capstone Project**: Building an autonomous humanoid with voice-to-action capabilities

## Target Audience

- Students and developers learning Physical AI
- Readers with basic Python + AI knowledge entering robotics
- Practitioners seeking hands-on ROS 2, simulation, and VLA integration experience

## Technical Stack

- **ROS 2 Humble Hawksbill** (LTS, support until May 2027)
- **Gazebo Classic 11** for physics simulation
- **NVIDIA Isaac Sim 2023.1.0+** for photorealistic simulation
- **OpenAI GPT-4 + Whisper APIs** for VLA systems
- **Python 3.10+** for all code examples

## Prerequisites

- Basic Python programming
- Fundamental AI/ML concepts
- Command line familiarity
- Linux Ubuntu 22.04 (or Windows WSL2)

## Building the Book

This book is built with [Docusaurus](https://docusaurus.io/).

### Installation

```bash
npm install
```

### Local Development

```bash
npm start
```

This command starts a local development server and opens a browser window. Most changes are reflected live without needing to restart the server.

### Build

```bash
npm run build
```

This command generates static content into the `build` directory, which can be deployed to GitHub Pages.

### Deployment

The book automatically deploys to GitHub Pages via GitHub Actions on push to the main branch.

## License

MIT License (for code) / CC-BY 4.0 (for content)

## Contributing

This book was generated using [Spec-Kit Plus](https://github.com/spec-kit) and Claude Code, demonstrating an AI-driven content creation workflow.

## Project Structure

```
docs/                       # Book content (Markdown)
├── intro/                  # Introductory section
├── foundations/            # Foundational concepts
├── module-01-ros2/         # Module 1: ROS 2
├── module-02-digital-twin/ # Module 2: Simulation
├── module-03-isaac/        # Module 3: NVIDIA Isaac
├── module-04-vla/          # Module 4: VLA Systems
├── capstone/               # Capstone project
└── code-examples/          # Executable Python code

specs/                      # Design documents
└── 001-physical-ai-book/   # Specification, plan, tasks

.specify/                   # Spec-Kit Plus templates
history/prompts/            # Development history (PHRs)
```

## Learning Path

1. **Foundations** → Physical AI concepts, sensors, actuators
2. **Module 1** → ROS 2 architecture and Python programming
3. **Module 2** → Simulation with Gazebo and Unity
4. **Module 3** → NVIDIA Isaac for advanced robotics
5. **Module 4** → Voice-Language-Action systems
6. **Capstone** → Build a complete autonomous humanoid

Each module includes:
- Prerequisites checklist
- Conceptual explanations (500-1200 words per chapter)
- Practical, executable code examples
- Validation exercises

## Support

For questions or issues, please open a GitHub issue.

---

**Generated with**: Spec-Kit Plus + Claude Code
**Demonstrates**: AI-driven technical documentation workflow
