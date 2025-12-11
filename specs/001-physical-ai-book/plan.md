# Implementation Plan: Physical AI Humanoid Robotics Technical Book

**Branch**: `001-physical-ai-book` | **Date**: 2025-12-07 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-physical-ai-book/spec.md`

## Summary

Create a comprehensive, beginner-friendly technical book covering Physical AI and humanoid robotics, structured as 4 progressive modules with 12 total chapters. The book will guide readers from foundational Physical AI concepts through advanced Vision-Language-Action (VLA) systems, using ROS 2 Humble, Gazebo/Unity simulation, NVIDIA Isaac, and OpenAI GPT-4 integration. All content will be generated using Spec-Kit Plus + Claude Code workflows, compiled with Docusaurus, and deployed to GitHub Pages.

## Technical Context

**Language/Version**: Markdown (Docusaurus-compatible), Python 3.10+ for code examples
**Primary Dependencies**:
- ROS 2 Humble Hawksbill (LTS, support until May 2027)
- Gazebo (version compatible with ROS 2 Humble, e.g., Gazebo Classic 11 or Gazebo Fortress)
- Unity 2022 LTS or later (for HRI visualization examples)
- NVIDIA Isaac Sim 2023.1.0+ (supports ROS 2 Humble)
- OpenAI Python SDK (for GPT-4 API integration in VLA module)
- Whisper API (for voice recognition in VLA module)

**Storage**: Static Markdown files in Docusaurus structure; code examples as inline snippets or separate `.py` files
**Testing**:
- Docusaurus build validation (zero errors)
- Code example execution verification on ROS 2 Humble
- Technical accuracy review by robotics expert
- Test reader completion of modules

**Target Platform**: GitHub Pages (static site deployment), reader development environment (Linux Ubuntu 22.04 preferred, Windows WSL2 secondary)
**Project Type**: Technical documentation/educational content (Docusaurus static site)
**Performance Goals**:
- Site build time < 60 seconds
- Page load time < 2 seconds on 3G connection
- All code examples execute in < 30 seconds (excluding AI API latency)

**Constraints**:
- Each chapter: 500-1200 words
- No proprietary content or external copyrighted materials
- No analytics tracking (privacy-first)
- Environment variables for all API keys (never hardcoded)
- All content generated through Spec-Kit Plus workflows

**Scale/Scope**:
- 12 chapters across 4 modules
- 1 introductory section + 1 concluding section with capstone
- Estimated 15-20 code examples total
- 1 comprehensive capstone project (Voice → Plan → Navigate → Manipulate pipeline)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Note**: The constitution template is currently a placeholder. Since this is a documentation/book project rather than software, traditional constitution checks (library-first, CLI interface, TDD) do not apply. Instead, we enforce quality gates specific to technical writing:

### Documentation Quality Gates

✅ **Clarity-First**: Every concept explained in beginner-friendly language before technical details
✅ **Progressive Complexity**: Each module builds on previous knowledge; no forward references to unexplained concepts
✅ **Example-Driven**: Every chapter includes executable, copy-ready code examples (non-negotiable)
✅ **Technical Accuracy**: All ROS 2, Gazebo, Isaac, and VLA content must be syntactically and conceptually correct
✅ **No Implementation Leaks**: Book describes "what" and "why," not internal authoring process
✅ **Privacy & Security**: No analytics tracking; teach secure credential management
✅ **Docusaurus Compatibility**: All Markdown must compile without errors

**Gate Status**: ✅ **PASS** - All gates align with spec requirements (FR-012 to FR-030, SC-001 to SC-010)

## Project Structure

### Documentation (this feature)

```text
specs/001-physical-ai-book/
├── plan.md                  # This file (/sp.plan command output)
├── research.md              # Phase 0 output - Technical research on ROS 2, Gazebo, Isaac, VLA
├── book-architecture.md     # Phase 1 output - Detailed chapter structure and flow
├── content-outline.md       # Phase 1 output - Per-chapter outlines with learning objectives
├── quality-checklist.md     # Phase 1 output - Validation criteria for each chapter
├── checklists/              # Quality validation checklists
│   └── requirements.md      # Existing requirements checklist from spec phase
└── tasks.md                 # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Book Content (repository root - to be created during implementation)

```text
docs/                        # Docusaurus docs directory
├── intro/
│   ├── what-is-physical-ai.md
│   ├── embodied-intelligence.md
│   ├── digital-vs-physical-ai.md
│   └── robotics-landscape.md
│
├── foundations/
│   ├── sensors.md           # LiDAR, depth cameras, IMUs
│   ├── actuators.md         # Motors, servos, force/torque systems
│   └── digital-twin.md      # Sim-to-real pipeline
│
├── module-01-ros2/
│   ├── _category_.json      # Module metadata for Docusaurus
│   ├── prerequisites.md     # Prerequisites checklist
│   ├── 01-ros2-architecture.md
│   ├── 02-python-controllers.md
│   └── 03-urdf-humanoids.md
│
├── module-02-digital-twin/
│   ├── _category_.json
│   ├── prerequisites.md
│   ├── 01-physics-simulation.md
│   ├── 02-gazebo-testing.md
│   └── 03-unity-visualization.md
│
├── module-03-isaac/
│   ├── _category_.json
│   ├── prerequisites.md
│   ├── 01-isaac-sim.md
│   ├── 02-isaac-ros.md
│   └── 03-nav2-planning.md
│
├── module-04-vla/
│   ├── _category_.json
│   ├── prerequisites.md
│   ├── 01-voice-to-action.md
│   ├── 02-llm-planning.md
│   └── 03-capstone.md
│
├── capstone/
│   ├── architecture.md      # Full system architecture
│   ├── integration.md       # Voice → Plan → Navigate → Manipulate
│   └── next-steps.md        # Career pathways, additional resources
│
└── code-examples/           # Standalone Python files for testing
    ├── ros2/
    │   ├── simple_publisher.py
    │   ├── simple_subscriber.py
    │   └── basic_humanoid.urdf
    ├── gazebo/
    │   └── spawn_robot.py
    ├── isaac/
    │   └── synthetic_data_gen.py
    └── vla/
        ├── .env.example
        ├── whisper_listener.py
        ├── gpt4_planner.py
        └── full_pipeline.py

docusaurus.config.js         # Docusaurus configuration
sidebar.js                   # Navigation structure
package.json                 # Node dependencies for Docusaurus
```

**Structure Decision**: Docusaurus static site with hierarchical docs structure. Each module is a top-level category with 3 chapters. Introductory and capstone sections bookend the main modules. Code examples live in separate directory for standalone testing and are referenced/embedded in chapter Markdown files.

## Complexity Tracking

No constitution violations - this is a documentation project, not software.

---

## Phase 0: Research & Technical Foundations

### Research Objectives

Research is divided into 5 domains aligned with book modules:

#### 1. Physical AI Foundations Research
**Goal**: Understand core concepts to explain in introductory section

**Tasks**:
- Define Physical AI vs traditional AI (embodied intelligence, sensor-motor loops)
- Identify 3-5 key differentiators (real-world interaction, physics constraints, latency requirements)
- Research humanoid robotics landscape (Boston Dynamics, Figure AI, Tesla Optimus - high-level only)
- Document sensor types and use cases (LiDAR for SLAM, depth cameras for object detection, IMUs for balance)
- Document actuator types (DC motors, servos, linear actuators - conceptual only)
- Research sim-to-real transfer techniques (domain randomization, reality gap concepts)

**Output**: `research.md` section "Physical AI Foundations"

#### 2. ROS 2 Humble Technical Research
**Goal**: Verify ROS 2 Humble architecture details for accurate Module 1 content

**Tasks**:
- Confirm ROS 2 Humble node communication patterns (DDS middleware, pub/sub, services, actions)
- Research rclpy API for beginners (minimal publisher/subscriber examples)
- Document URDF XML structure for humanoid models (joints, links, sensors, collision/visual geometry)
- Identify common ROS 2 Humble + Python gotchas for beginners (callback groups, QoS settings)
- Find official ROS 2 Humble installation instructions (Ubuntu 22.04, Windows WSL2)

**Output**: `research.md` section "ROS 2 Humble Architecture & rclpy"

#### 3. Simulation Stack Research (Gazebo + Unity)
**Goal**: Determine compatible versions and usage patterns for Module 2

**Tasks**:
- **Decision**: Gazebo Classic 11 vs Gazebo Fortress/Garden for ROS 2 Humble
  - **Options**:
    - Gazebo Classic 11 (mature, extensive tutorials, officially deprecated but widely used)
    - Gazebo Fortress (newer, better performance, less beginner documentation)
  - **Recommendation**: Gazebo Classic 11 (more accessible for beginners despite deprecation)
  - **Rationale**: Clearer beginner tutorials; book focuses on concepts, not bleeding-edge tools

- Research Gazebo physics engine configuration (gravity, collision, friction, damping)
- Research Gazebo + ROS 2 integration (gazebo_ros_pkgs, spawning models from URDF)
- Research Unity + ROS 2 integration options (ROS-TCP-Connector, Unity Robotics Hub)
- **Decision**: Unity role in book
  - **Options**:
    - Full tutorial on Unity-ROS 2 integration (complex, high setup overhead)
    - Conceptual overview with when to use Unity vs Gazebo (simpler, focus on decision-making)
  - **Recommendation**: Conceptual overview only
  - **Rationale**: Keeps Module 2 Chapter 3 within 500-1200 words; focuses on "when" not "how"

**Output**: `research.md` section "Simulation Stack (Gazebo & Unity)"

#### 4. NVIDIA Isaac Research
**Goal**: Verify Isaac Sim + Isaac ROS compatibility with ROS 2 Humble for Module 3

**Tasks**:
- Confirm Isaac Sim version supporting ROS 2 Humble (Isaac Sim 2023.1.0+)
- Research Isaac Sim synthetic data generation workflow (replicator API, annotation formats)
- Research Isaac ROS 2 packages (isaac_ros_visual_slam, isaac_ros_depth_processing, isaac_ros_nvblox)
- Research Nav2 integration with ROS 2 Humble (navigation stack, behavior trees, costmaps)
- Identify GPU requirements (NVIDIA RTX series minimum for Isaac Sim)
- **Decision**: CPU alternatives for readers without NVIDIA GPU
  - **Options**:
    - Recommend cloud GPU services (AWS, Google Colab with GPU)
    - Skip Isaac module for CPU-only users
  - **Recommendation**: Note cloud alternatives; keep Isaac module accessible
  - **Rationale**: Aligns with edge case from spec (FR-104)

**Output**: `research.md` section "NVIDIA Isaac (Sim + ROS)"

#### 5. VLA System Research (Whisper + GPT-4)
**Goal**: Research voice-language-action pipeline for Module 4

**Tasks**:
- Research OpenAI Whisper API usage (audio input formats, transcription accuracy, latency)
- Research OpenAI GPT-4 API for action planning (prompt engineering for robotic task decomposition)
- Research ROS 2 action servers (actionlib patterns in ROS 2, goal/feedback/result messages)
- Document environment variable best practices (python-dotenv, .env.example templates)
- Estimate OpenAI API costs for capstone project (tokens per task, pricing tiers)
- **Decision**: Diagram format for capstone architecture
  - **Options**:
    - Mermaid diagrams (embedded in Markdown, version-controllable, simple syntax)
    - PNG/SVG images (higher fidelity, requires external tools)
  - **Recommendation**: Mermaid diagrams
  - **Rationale**: Aligns with constraint "no external proprietary content," easier to maintain

**Output**: `research.md` section "VLA System (Whisper + GPT-4 + ROS 2 Actions)"

#### 6. Docusaurus Setup Research
**Goal**: Determine Docusaurus configuration for book deployment

**Tasks**:
- Research Docusaurus v3 installation and configuration
- Research GitHub Pages deployment workflow (build, deploy action)
- Research Docusaurus sidebar configuration (hierarchical categories, custom labels)
- Verify Mermaid plugin for Docusaurus (diagrams support)
- **Decision**: Docusaurus theme and plugins
  - **Options**:
    - Classic theme (default, well-documented)
    - Custom theme (more control, higher complexity)
  - **Recommendation**: Classic theme with minimal customization
  - **Rationale**: Simplicity aligns with constitution; focus on content not styling

**Output**: `research.md` section "Docusaurus Configuration & Deployment"

### Research Validation Criteria

Each research section must answer:
- ✅ What is the recommended version/tool for beginners?
- ✅ What are the key concepts readers must understand?
- ✅ What are common beginner mistakes to avoid?
- ✅ What are minimum system requirements (if applicable)?
- ✅ Where are official documentation sources?

---

## Phase 1: Book Architecture & Content Design

### 1. Book Architecture (`book-architecture.md`)

**Structure**:

```text
I. Front Matter
   - Title, Author, Version, License (MIT or CC-BY)
   - Prerequisites (Python, AI/ML basics, command line)
   - How to Use This Book (progressive reading vs module jumping)

II. Introductory Section (4 sub-sections, ~3000 words total)
   A. What is Physical AI?
   B. Why Embodied Intelligence Matters
   C. Digital AI vs Physical-World AI
   D. Overview of Humanoid Robotics Landscape

III. Foundational Concepts (3 sub-sections, ~2000 words total)
   A. Sensors (LiDAR, Depth Cameras, IMUs)
   B. Actuators (Motors, Servos, Force/Torque Systems)
   C. Digital Twin and Sim-to-Real Pipeline

IV. Module 1: The Robotic Nervous System (ROS 2)
   Prerequisites Checklist:
   - [ ] Python 3.10+ installed
   - [ ] Basic object-oriented programming understanding
   - [ ] Command line familiarity

   Chapter 1: Understanding ROS 2 Architecture (800 words)
   - Nodes, topics, services, actions
   - DDS middleware overview
   - When to use each communication pattern

   Chapter 2: Building Python Controllers with rclpy (1000 words)
   - Creating publishers and subscribers
   - Callback functions and spin
   - Example: velocity command publisher

   Chapter 3: URDF for Humanoids (900 words)
   - XML structure (links, joints, sensors)
   - Collision vs visual geometry
   - Example: simple bipedal robot URDF

V. Module 2: The Digital Twin (Gazebo & Unity)
   Prerequisites Checklist:
   - [ ] Completed Module 1 (ROS 2)
   - [ ] Understanding of 3D coordinate systems
   - [ ] Basic physics concepts (gravity, friction)

   Chapter 1: Physics Simulation Fundamentals (750 words)
   - Gravity, collision, dynamics properties
   - Time-stepping and numerical integration
   - Physics engine configuration

   Chapter 2: Building and Testing Robots in Gazebo (1100 words)
   - Spawning URDF models in Gazebo
   - Applying forces and torques
   - Sensor simulation (cameras, LiDAR)

   Chapter 3: High-Fidelity Visualization and HRI in Unity (600 words)
   - When to use Unity vs Gazebo
   - Unity-ROS 2 integration overview (conceptual)
   - HRI visualization examples

VI. Module 3: The AI-Robot Brain (NVIDIA Isaac)
   Prerequisites Checklist:
   - [ ] Completed Modules 1 & 2
   - [ ] NVIDIA GPU (RTX series) or cloud GPU access
   - [ ] Isaac Sim 2023.1.0+ installed

   Chapter 1: Isaac Sim for Photorealistic Simulation (950 words)
   - Creating photorealistic scenes
   - Synthetic data generation (Replicator API)
   - Labeled data export for training

   Chapter 2: Isaac ROS: Accelerated Perception + VSLAM (1050 words)
   - isaac_ros_visual_slam setup
   - GPU-accelerated depth processing
   - Integration with ROS 2 Humble

   Chapter 3: Nav2 Path Planning for Humanoid Locomotion (850 words)
   - Nav2 stack overview
   - Costmap configuration
   - Obstacle avoidance for bipedal robots

VII. Module 4: Vision-Language-Action (VLA)
   Prerequisites Checklist:
   - [ ] Completed Modules 1-3
   - [ ] OpenAI API key (free tier or paid)
   - [ ] Understanding of environment variables

   Chapter 1: Voice-to-Action with Whisper (700 words)
   - Whisper API integration
   - Audio input → text transcription
   - Parsing commands into ROS 2 actions

   Chapter 2: LLM-Based Cognitive Planning (1000 words)
   - GPT-4 API for task decomposition
   - Natural language → action sequences
   - Example: "Pick up the red block" → plan

   Chapter 3: Capstone — Building the Autonomous Humanoid (1200 words)
   - Full pipeline: Voice → Plan → Navigate → Manipulate
   - System integration (Whisper + GPT-4 + Nav2 + Isaac ROS)
   - Testing and validation

VIII. Capstone Section (3 sub-sections, ~2000 words total)
   A. Full System Architecture (Mermaid diagram + explanation)
   B. Integration Workflow (Voice → Cognitive Plan → Robot Action)
   C. Career Pathways in Physical AI (resources, companies, research areas)

IX. Back Matter
   - Glossary of Terms
   - Additional Resources (official docs, papers, tutorials)
   - Acknowledgments
```

**Total Word Count Estimate**: ~14,500 words across 12 chapters + intro/capstone sections

### 2. Content Outline (`content-outline.md`)

For each of the 12 chapters, define:
- **Learning Objectives** (3-5 bullet points)
- **Key Concepts** (terms to define)
- **Code Examples** (title and purpose)
- **Common Pitfalls** (beginner mistakes to address)
- **Validation Questions** (self-check for readers)

Example for Module 1, Chapter 1:

```markdown
## Module 1, Chapter 1: Understanding ROS 2 Architecture

**Learning Objectives**:
- Explain the role of nodes, topics, services, and actions in ROS 2
- Diagram a simple publisher-subscriber system
- Identify when to use topics vs services vs actions
- Understand DDS middleware at a high level

**Key Concepts**:
- Node: Independent process performing computation
- Topic: Named bus for asynchronous message passing
- Service: Synchronous request-reply communication
- Action: Long-running tasks with feedback
- DDS: Data Distribution Service (middleware layer)
- QoS: Quality of Service policies

**Code Examples**:
1. Minimal publisher example (Python rclpy)
2. Minimal subscriber example (Python rclpy)
3. Service client-server example (conceptual, not full code)

**Common Pitfalls**:
- Confusing topics (pub/sub) with services (req/reply)
- Not sourcing ROS 2 environment before running nodes
- Incorrect QoS settings causing message loss

**Validation Questions**:
1. When should you use a topic vs a service?
2. What is the role of DDS in ROS 2?
3. Can multiple nodes subscribe to the same topic? (Yes)
```

Repeat this structure for all 12 chapters.

### 3. Quality Validation Checklist (`quality-checklist.md`)

Define per-chapter validation criteria aligned with success criteria (SC-001 to SC-010):

**Per-Chapter Checklist**:

```markdown
# Chapter Validation Checklist

For each chapter, verify:

## Content Quality
- [ ] Word count: 500-1200 words ✓ (SC-001)
- [ ] Beginner-friendly language (no unexplained jargon) ✓ (FR-012)
- [ ] Technical jargon defined on first use ✓ (FR-015)
- [ ] Progressive complexity (builds on prior chapters) ✓ (FR-014)
- [ ] No deep mathematical proofs ✓ (FR-016)
- [ ] Focus on applied learning ✓ (FR-017)

## Code Examples
- [ ] At least one practical code example included ✓ (FR-013, SC-008)
- [ ] Code is syntactically correct Python (rclpy) ✓ (FR-007)
- [ ] Code is copy-ready (no placeholders requiring modification) ✓ (FR-013)
- [ ] Code examples execute without errors on ROS 2 Humble ✓ (SC-003)
- [ ] Comments explain key lines ✓ (FR-013)

## Technical Accuracy
- [ ] ROS 2 Humble architecture accurately represented ✓ (FR-006)
- [ ] URDF examples produce valid robot models ✓ (FR-008)
- [ ] Simulation examples work with Gazebo/Unity versions ✓ (FR-009)
- [ ] Isaac Sim workflows compatible with documented versions ✓ (FR-010)
- [ ] VLA examples demonstrate working pipelines ✓ (FR-011)

## Security & Credentials
- [ ] API keys use environment variables (if applicable) ✓ (FR-026)
- [ ] .env.example template provided (if applicable) ✓ (FR-027)
- [ ] Secure practices taught appropriately ✓ (FR-028)

## Docusaurus Compatibility
- [ ] Markdown compiles without errors ✓ (SC-002)
- [ ] Mermaid diagrams render correctly (if applicable)
- [ ] Code blocks use correct syntax highlighting
- [ ] Links to other chapters work correctly

## Module Integration
- [ ] Prerequisites checklist at module start ✓ (FR-030)
- [ ] Consistent with overall module flow ✓ (SC-009)
- [ ] No forward references to unexplained concepts ✓ (FR-014)

## Final Verification
- [ ] Passes technical review by robotics expert ✓ (SC-007)
- [ ] Test reader can complete chapter and apply concepts ✓ (SC-005, SC-006)
```

**Capstone Integration Test**:

```markdown
# Capstone Validation Checklist

Module 4, Chapter 3 (Capstone) must demonstrate:

- [ ] Voice input → Whisper transcription working
- [ ] Whisper output → GPT-4 task planning working
- [ ] GPT-4 plan → ROS 2 action sequences working
- [ ] Nav2 navigation → obstacle avoidance working
- [ ] Object detection → manipulation planning working
- [ ] Full pipeline: "Pick up the red block" → robot action
- [ ] Environment variables properly configured
- [ ] System integration documented with Mermaid diagram

This validates SC-006: "Test reader can complete capstone and demonstrate voice-to-action system"
```

---

## Key Architectural Decisions

### Decision 1: Simulation Stack Choice

**Question**: Which simulation tools to emphasize in Module 2?

**Options**:
| Option | Pros | Cons |
|--------|------|------|
| Gazebo Classic 11 only | Mature, extensive tutorials, widely used | Officially deprecated, older architecture |
| Gazebo Fortress/Garden only | Newer, better performance, modern architecture | Less beginner documentation, steeper learning curve |
| Both Gazebo + Unity equally | Comprehensive coverage | Too broad for 3-chapter module, dilutes focus |
| Gazebo primary, Unity conceptual | Balances practical skills with awareness | Unity coverage limited to "when to use" |

**Chosen**: **Gazebo Classic 11 primary, Unity conceptual overview**

**Rationale**:
- Gazebo Classic has clearer beginner tutorials despite deprecation
- Book teaches concepts (physics simulation, ROS 2 integration) that apply to any simulator
- Unity chapter focuses on decision-making ("when Unity vs Gazebo") rather than full tutorial
- Keeps Module 2 within scope (each chapter 500-1200 words)

**Tradeoffs**:
- Readers won't get hands-on Unity-ROS 2 integration
- Gazebo Classic deprecation means eventual migration needed
- Accepted because: Book prioritizes learning fundamentals over tool-specific training

---

### Decision 2: ROS 2 Version & Python Tooling

**Question**: Which ROS 2 distribution and what depth of rclpy coverage?

**Options**:
| Option | Pros | Cons |
|--------|------|------|
| ROS 2 Humble (LTS) | Long support (until 2027), stable, beginner-friendly | Not the absolute latest |
| ROS 2 Iron/Jazzy | Newest features | Shorter support window, more changes |
| Cover multiple ROS 2 versions | Comprehensive | Confusing for beginners, exceeds word limits |
| rclpy deep dive (all APIs) | Thorough understanding | Too much detail for 1000-word chapter |
| rclpy basics only (pub/sub/service) | Focused, achievable | Limited advanced patterns |

**Chosen**: **ROS 2 Humble (LTS) + rclpy basics (pub/sub focus)**

**Rationale**:
- ROS 2 Humble LTS provides stability for educational content (spec clarification from /sp.clarify)
- Focus on publisher/subscriber patterns (most common in robotics)
- Services and actions introduced conceptually, not exhaustively
- Aligns with FR-017 (applied learning over theoretical completeness)

**Tradeoffs**:
- Readers won't learn advanced rclpy patterns (lifecycle nodes, parameter services)
- Accepted because: Book targets beginners; advanced patterns accessible in official ROS 2 docs

---

### Decision 3: Scope Boundaries (Applied vs Deep Theory)

**Question**: How deep into robotics theory (kinematics, dynamics, control)?

**Options**:
| Option | Pros | Cons |
|--------|------|------|
| Include kinematics/dynamics math | Comprehensive theoretical foundation | Violates FR-016 (no deep math), alienates beginners |
| Applied only (no equations) | Accessible, aligns with spec | Less rigorous, skips "why" behind algorithms |
| Conceptual theory (diagrams, not equations) | Balances understanding and accessibility | Some readers want mathematical rigor |

**Chosen**: **Applied robotics with conceptual theory (diagrams, no equations)**

**Rationale**:
- FR-016 explicitly prohibits deep mathematical proofs
- FR-017 mandates applied learning over theoretical completeness
- Readers with basic Python + AI background (not robotics PhDs)
- Concepts explained with Mermaid diagrams and analogies, not linear algebra

**Tradeoffs**:
- Readers won't derive forward kinematics or dynamics equations
- Accepted because: Spec explicitly constrains scope to applied learning (FR-016, FR-017)

---

### Decision 4: Diagram Formats (Mermaid vs Images)

**Question**: How to create diagrams for architecture, workflows, and systems?

**Options**:
| Option | Pros | Cons |
|--------|------|------|
| Mermaid (text-based diagrams) | Version-controllable, Docusaurus-native, no external tools | Limited visual fidelity, learning curve |
| PNG/SVG images (draw.io, Figma) | High fidelity, more expressive | Requires external tools, harder to update, not version-friendly |
| Both (Mermaid for flows, images for complex diagrams) | Best of both worlds | Inconsistent style, more tooling |

**Chosen**: **Mermaid diagrams exclusively**

**Rationale**:
- FR-022 prohibits external proprietary content (Figma, licensed images)
- Mermaid is Docusaurus-native (plugin available)
- Version-controllable (text-based, Git-friendly)
- Aligns with Spec-Kit Plus workflow (all content in Markdown)

**Tradeoffs**:
- Mermaid has limited expressiveness for complex 3D robot diagrams
- Accepted because: Book focuses on system architecture and workflows (which Mermaid handles well), not mechanical CAD (which is out-of-scope per FR-020)

---

### Decision 5: Hardware Description Detail Level

**Question**: How much detail on physical robot hardware (motors, sensors, mechanical design)?

**Options**:
| Option | Pros | Cons |
|--------|------|------|
| Full hardware buying guide | Practical for builders | Violates FR-018, scope creep |
| Detailed mechanical specs | Technical depth | Violates FR-020 (no CAD), exceeds beginner level |
| High-level overview (sensor/actuator types) | Conceptual understanding | Readers can't build physical robot |
| No hardware discussion | Focused on software | Misses Physical AI embodiment aspect |

**Chosen**: **High-level overview of sensor/actuator types (no buying guide, no CAD)**

**Rationale**:
- FR-018 explicitly prohibits full hardware buying guides (brief summaries acceptable)
- FR-020 prohibits detailed mechanical CAD instructions
- Foundational Concepts section covers sensor types (LiDAR, cameras, IMUs) and actuator types (motors, servos) conceptually
- Focus on software integration (ROS 2, simulation, AI) not hardware engineering

**Tradeoffs**:
- Readers can't directly build a physical humanoid from this book
- Accepted because: Spec defines this as a software/AI book, not mechanical engineering guide

---

## Testing Strategy

### Per-Chapter Validation

**For each of 12 chapters, validate against**:

1. **Clarity for Beginners** (SC-005):
   - Test reader with Python + AI background (no robotics experience) attempts chapter
   - Can reader complete chapter without external research?
   - Are technical terms defined on first use? (FR-015)
   - Is progressive complexity maintained? (FR-014)

2. **Technical Correctness** (SC-003, SC-007):
   - All code examples execute without errors on ROS 2 Humble environment
   - URDF examples load in ROS 2 without warnings
   - Robotics expert reviews content for accuracy (SC-007)
   - Verify against official ROS 2 Humble, Gazebo, Isaac docs

3. **Word Count Structure** (SC-001):
   - Run `wc -w chapter.md` for each chapter
   - Verify 500-1200 word range (excluding code blocks)
   - If over 1200: identify cuts; if under 500: expand with examples

4. **Docusaurus Build** (SC-002):
   - Run `npm run build` after each chapter added
   - Zero errors required to pass
   - Verify Mermaid diagrams render correctly
   - Check navigation sidebar updates correctly

5. **Module Flow Consistency** (SC-009):
   - Does chapter reference concepts from prior chapters only? (no forward refs)
   - Does chapter align with module prerequisites checklist? (FR-030)
   - Does chapter fit within module learning arc?

### Integration Testing

**After all 12 chapters complete**:

1. **Full Docusaurus Build**:
   - `npm run build` completes with zero errors (SC-002)
   - All internal links resolve correctly
   - Sidebar navigation functional

2. **GitHub Pages Deployment**:
   - Deploy to GitHub Pages via GitHub Actions
   - Site is publicly accessible (SC-004)
   - No analytics tracking present (FR-029)

3. **Capstone Integration Test** (SC-006):
   - Test reader attempts Module 4 Chapter 3 capstone
   - Validates full pipeline: Voice → Plan → Navigate → Manipulate
   - System components:
     - Whisper API transcribes voice command
     - GPT-4 API generates action plan
     - ROS 2 action server executes plan
     - Nav2 navigates to target
     - Object detection triggers manipulation
   - Success: Reader demonstrates working voice-to-action system

4. **Technical Review** (SC-007):
   - Robotics expert reviews all 12 chapters
   - Validates accuracy of ROS 2, Gazebo, Isaac, VLA content
   - Checks for misleading simplifications or errors
   - Sign-off required before publication

5. **Test Reader Completion** (SC-005, SC-006):
   - Recruit 2-3 test readers (Python + AI background, no robotics)
   - Readers attempt Module 1 (ROS 2): verify they create working node + URDF
   - Readers attempt capstone: verify they demonstrate voice-to-action system
   - Collect feedback on clarity, difficulty, gaps

---

## Writing Phases

### Phase 1: Research (Complete Before Writing)

**Deliverable**: `research.md` with all 6 research domains documented

**Activities**:
- Perform research tasks outlined in Phase 0 section above
- Document decisions with options, tradeoffs, justifications
- Resolve all "NEEDS CLARIFICATION" items from Technical Context
- Validate research findings against official documentation

**Duration Estimate**: Research concurrent with planning (complete by end of /sp.plan phase)

### Phase 2: Foundation (Book Architecture)

**Deliverable**: `book-architecture.md` + `content-outline.md` + `quality-checklist.md`

**Activities**:
- Define full book structure (intro → modules → capstone)
- Create per-chapter outlines with learning objectives
- Define validation checklist for each chapter
- Set up Docusaurus project structure (empty docs/ directory)

**Duration Estimate**: Part of /sp.plan phase (this document)

### Phase 3: Analysis (Per-Module Breakdown) - NOT STARTED IN /sp.plan

**Deliverable**: Detailed chapter insights and tradeoff documentation (deferred to /sp.tasks)

**Activities** (for /sp.tasks phase):
- Break each module into granular writing tasks
- Identify dependencies between chapters
- Plan code example development
- Define acceptance tests per chapter

**Duration Estimate**: To be determined in /sp.tasks

### Phase 4: Synthesis (Content Writing) - NOT STARTED IN /sp.plan

**Deliverable**: Final Docusaurus-compatible Markdown chapters (deferred to implementation)

**Activities** (for implementation phase):
- Write all 12 chapters following outlines
- Develop and test all code examples
- Create Mermaid diagrams
- Run per-chapter validation checklists
- Iterate based on test reader feedback

**Duration Estimate**: To be determined during implementation

---

## Constraints & Quality Gates

### Content Constraints (from FR-018 to FR-022)

✅ **No hardware buying guides** (brief summaries acceptable)
✅ **No multi-robot swarm** (single humanoid focus)
✅ **No detailed CAD** (conceptual hardware only)
✅ **No deep CUDA** (Isaac ROS usage, not CUDA programming)
✅ **Original/open-source content only** (no proprietary materials)

### Security Constraints (from FR-026 to FR-029)

✅ **Environment variables for API keys** (never hardcode)
✅ **.env.example template** (provided in VLA module)
✅ **Teach secure practices** (appropriate for beginners)
✅ **No analytics tracking** (privacy-first deployment)

### Workflow Constraints (from FR-023 to FR-025)

✅ **Spec-Kit Plus + Claude Code** (all content generated via workflows)
✅ **Docusaurus builds successfully** (zero errors gate)
✅ **GitHub Pages deployable** (static site ready)

---

## Success Criteria Mapping

| Success Criterion | Validation Method | Gate |
|-------------------|-------------------|------|
| SC-001: 12 chapters, 500-1200 words each | `wc -w` per chapter | Per-chapter checklist |
| SC-002: Docusaurus builds with zero errors | `npm run build` | Integration test |
| SC-003: Code examples execute on ROS 2 Humble | Run all .py files in test environment | Per-chapter checklist |
| SC-004: Site deploys to GitHub Pages | GitHub Actions deployment | Integration test |
| SC-005: Test reader completes Module 1 | Test reader validation | Integration test |
| SC-006: Test reader completes capstone | Test reader validation | Capstone integration test |
| SC-007: Passes robotics expert review | Expert sign-off | Integration test |
| SC-008: All chapters have code examples | Per-chapter checklist | Per-chapter checklist |
| SC-009: Navigable structure | Docusaurus sidebar validation | Integration test |
| SC-010: Demonstrates Spec-Kit workflow | PHR records + artifacts | Meta-validation |

---

## Next Steps (After /sp.plan)

1. **Review this plan** - Verify alignment with spec and clarifications
2. **Run `/sp.tasks`** - Generate granular, dependency-ordered tasks for implementation
3. **Set up Docusaurus project** - Initialize docs/ structure, configure docusaurus.config.js
4. **Begin Phase 3 (Analysis)** - Break modules into implementable tasks
5. **Proceed to implementation** - Write chapters following quality checklists

---

---

## Architectural Decision Records — Intelligence Suggestion

After completing the planning work, the following decisions meet the three-part ADR significance test (Impact, Alternatives, Scope):

### 📋 Architectural Decision 1: Docusaurus Theme and Deployment Strategy

**Brief**: Choosing Docusaurus classic theme with GitHub Pages deployment over alternatives like GitBook, MkDocs, or custom React site.

**Three-Part Test**:
- ✅ **Impact**: Long-term consequences for content authoring workflow, deployment automation, and reader navigation experience
- ✅ **Alternatives**: Multiple viable options (Docusaurus, GitBook, MkDocs, custom site) with significant tradeoffs
- ✅ **Scope**: Cross-cutting decision affecting entire book infrastructure, authoring process, and deployment pipeline

**Suggestion**: 📋 Architectural decision detected: Docusaurus theme and GitHub Pages deployment strategy — Document reasoning and tradeoffs? Run `/sp.adr docusaurus-deployment-strategy`

---

### 📋 Architectural Decision 2: Research-Concurrent vs Waterfall Research Workflow

**Brief**: Conducting mini-research during chapter writing instead of upfront waterfall research phase.

**Three-Part Test**:
- ✅ **Impact**: Long-term consequences for development velocity, content accuracy, and workflow complexity
- ✅ **Alternatives**: Research-concurrent vs waterfall research vs post-hoc verification — each with different risk/speed tradeoffs
- ✅ **Scope**: Influences entire Spec-Kit Plus workflow execution and quality assurance strategy

**Suggestion**: 📋 Architectural decision detected: Research-concurrent workflow for content development — Document reasoning and tradeoffs? Run `/sp.adr research-concurrent-workflow`

---

### 📋 Architectural Decision 3: ROS 2 Humble LTS Version Selection

**Brief**: Using ROS 2 Humble Hawksbill (LTS, support until May 2027) instead of latest ROS 2 release or older versions.

**Three-Part Test**:
- ✅ **Impact**: Long-term consequences for code example longevity, tool compatibility, and book lifespan
- ✅ **Alternatives**: ROS 2 Humble (LTS) vs Iron/Jazzy (latest) vs Foxy (older LTS) — different support windows and feature sets
- ✅ **Scope**: Affects all code examples, dependency specifications, and reader onboarding experience across all modules

**Suggestion**: 📋 Architectural decision detected: ROS 2 Humble LTS version selection — Document reasoning and tradeoffs? Run `/sp.adr ros2-humble-version-selection`

---

### 📋 Architectural Decision 4: OpenAI GPT-4 API for VLA Module Examples

**Brief**: Using OpenAI GPT-4 API for LLM planning in VLA module instead of open-source LLMs or alternative providers.

**Three-Part Test**:
- ✅ **Impact**: Long-term consequences for reader accessibility (API costs), example reproducibility, and VLA module complexity
- ✅ **Alternatives**: OpenAI GPT-4 vs open-source LLMs (Llama 2) vs other providers (Anthropic, Google) — different cost/accessibility/documentation tradeoffs
- ✅ **Scope**: Influences Module 4 design, credential management approach, and capstone project feasibility for readers

**Suggestion**: 📋 Architectural decision detected: OpenAI GPT-4 API for VLA examples — Document reasoning and tradeoffs? Run `/sp.adr openai-gpt4-vla-selection`

---

### 📋 Architectural Decision 5: Simulation Stack — Gazebo Classic vs Gazebo Fortress

**Brief**: Using Gazebo Classic 11 as primary simulator despite official deprecation, with Unity as conceptual overview only.

**Three-Part Test**:
- ✅ **Impact**: Long-term consequences for example longevity (deprecated tool), beginner accessibility, and migration requirements
- ✅ **Alternatives**: Gazebo Classic 11 vs Gazebo Fortress/Garden vs equal coverage of Gazebo+Unity — different maturity/documentation tradeoffs
- ✅ **Scope**: Cross-cutting decision affecting Module 2 structure, code example complexity, and tutorial depth

**Suggestion**: 📋 Architectural decision detected: Gazebo Classic 11 as primary simulator with Unity conceptual coverage — Document reasoning and tradeoffs? Run `/sp.adr simulation-stack-selection`

---

**ADR Creation Protocol**: Wait for user consent before creating ADRs. These suggestions are provided for intelligent decision documentation, not automatic execution.

---

**Plan Version**: 1.1 | **Created**: 2025-12-07 | **Updated**: 2025-12-10 | **Status**: ✅ **COMPLETE** - Ready for `/sp.tasks` command

All research objectives defined, architectural decisions documented with ADR suggestions, quality gates established, and testing strategy planned.
