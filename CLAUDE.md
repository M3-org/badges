# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This repository is part of the **Meritverse** - a vision for transforming the internet into an MMORPG where online activities become quests with meaningful rewards. These 3D badges, pins, and patches serve as digital status symbols that represent real-world achievements, skills, and contributions rather than just financial wealth.

### The Meritverse Vision
- **Internet MMORPG**: Inspired by "The Great Online Game," integrating Discord roles, GitHub contributions, and crypto bounties
- **Achievement-Based Status**: Unlike financial status symbols (crypto punks, RuneScape party hats), these represent earned accomplishments
- **Skill Trees & Progression**: Building reputation systems similar to RuneScape's skill system and Capes of Accomplishment
- **Avatar Wearables**: Integrated with [Character Studio](https://m3-org.github.io/characterstudio-docs/docs/about/) for 3D avatar customization
- **Cross-Platform Identity**: Unifying disparate online activities into cohesive digital identity

### Integration Ecosystem
- **Dework/CharmVerse**: Task management with crypto bounties
- **Discord**: Role-based community progression
- **GitHub**: Contribution tracking and automated task creation
- **Character Studio**: Open-source avatar creation and wearable system
- **NFT Distribution**: M3rit collection on Zora/OpenSea (0x1a3a6e18f50FCc943b64D92098E1cA6B9b4d0812)

## Repository Structure

### Badge Categories & Progression
- **Skill Badges** (`dework/`): Role-based progression system
  - Admin, Community, Design, Dev, Legal, Marketing, Ops, Product, Research, Translation, Writing
  - Represents competency levels and specializations within DAOs/projects
- **Achievement Badges** (`remilia/`): Numbered collection (001-129) representing milestone achievements
- **Platform Badges**: Integration with various platforms and communities
  - `discord/`, `github/`, `blender/` - Platform-specific achievements
  - `m3/`, `metafactory/` - Community/project affiliations
- **Equipment/Inventory** (`backpack/`): Metaphorical inventory system for avatar customization
- **Root Level**: Individual achievement badges (`diamond-hands.glb`, `jokerace.glb`, etc.)

### Source Files & Templates
- **Master Templates**: 
  - `Skill-Badges-Master-File2.blend` - Main skill badge template with consistent styling
  - Individual .blend files for specific badge variants
- **Multi-Format Export**: GLB (web-optimized), FBX (game engine compatibility), .blend (source)
- **Procedural Generation**: Geometry nodes setup for consistent badge creation

### Logo Generation System
The `logo-generator/` directory contains an automated pipeline for converting 2D logos into 3D badge models:

#### Key Components
- `svg_to_glb.py` - Main conversion script (runs in Blender)
- `logo_automate.blend` - Template with geometry nodes setup
- Organized subdirectories for different platforms (linux/, msf/, etc.)
- PNG/SVG source files for various logos

#### Conversion Process
The Python script automates:
1. SVG import into Blender
2. Curve manipulation and geometry node application
3. UV mapping and material setup
4. PNG texture generation via ImageMagick
5. GLB export with proper materials

## Development Workflow

### Badge Creation Pipeline
1. **Design Phase**: Create or source 2D logos/designs (SVG preferred for automated conversion)
2. **Template Application**: Use master .blend files to maintain consistent badge styling
3. **Automated Conversion**: Use logo-generator pipeline for SVG → 3D badge conversion
4. **Manual Customization**: Fine-tune specific badges in Blender as needed
5. **Multi-Format Export**: Export to GLB (web), FBX (games), maintain .blend source

### Automated Logo-to-Badge Conversion
Convert SVG logos to 3D badges using the automated pipeline:
```bash
blender -b logo-generator/logo_automate.blend --python logo-generator/svg_to_glb.py -- -i input.svg -o output.glb
```

### Integration Workflow (Meritverse Context)
1. **Achievement Definition**: Define criteria for earning badges (GitHub contributions, Discord activity, task completion)
2. **Badge Assignment**: Integrate with Dework/Discord roles for automatic badge eligibility
3. **Character Studio Integration**: Load badges as wearables based on wallet ownership
4. **NFT Minting**: Mint completed badges to M3rit collection for permanent ownership

### Dependencies
- **Blender** (3D modeling and batch processing)
- **ImageMagick** (SVG to PNG conversion)
- **Python** (automation scripts)
- **Character Studio** (avatar integration)
- **Dework/Discord APIs** (achievement tracking)

## File Naming Conventions
- **Individual achievements**: Descriptive names reflecting the accomplishment (`diamond-hands.glb`, `jokerace.glb`)
- **Numbered series**: Zero-padded for collections (`001.glb`, `002.glb`) 
- **Platform badges**: Platform prefix for clear identification (`github_pin.glb`, `discord_pin.glb`)
- **Skill badges**: Role-based naming (`Admin_badge.glb`, `Dev_badge.glb`)

## Distribution & Integration Points

### Current Distribution
- **M3rit NFT Collection**: 0x1a3a6e18f50FCc943b64D92098E1cA6B9b4d0812
- **3D Preview Platform**: Sketchfab (https://skfb.ly/oFGqA)
- **NFT Marketplaces**: Zora, OpenSea
- **Open Source**: Free download from GitHub/Sketchfab for community use

### Future Integration Possibilities
- **POAP Integration**: Convert POAPs to wearable badges automatically
- **Wallet-Based Loading**: Character Studio reads owned badges from connected wallet
- **Skill Tree Visualization**: Progress tracking similar to RuneScape skill system
- **Cross-Platform Reputation**: Badges earned across GitHub, Discord, Dework, etc.
- **Procedural Generation**: Soulbound keyblades and loot based on wallet addresses
- **Guild/DAO Progression**: Team-based achievement systems

## Related Repositories
- **Character Studio**: [m3-org/CharacterStudio](https://github.com/m3-org/CharacterStudio) - Avatar creation and wearable system
- **ElizaOS Analytics**: GitHub-based reputation tracking and skill progression
- **AI News Aggregator**: Multi-platform activity aggregation for achievement tracking