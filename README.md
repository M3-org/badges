# Meritverse Badges

> 🎮 **Digital status symbols that can't be bought, only earned.**

Welcome to the Meritverse - where your real-world achievements, skills, and contributions transform into wearable digital badges for your avatar. Unlike financial status symbols, these 3D badges represent earned accomplishments in the Great Online Game.

## 🌟 Vision: Internet MMORPG

Inspired by RuneScape's progression system, we're building a reputation layer where:
- **Online activities become quests** with meaningful rewards
- **Skills and contributions** unlock wearable achievements
- **Cross-platform identity** unifies Discord roles, GitHub contributions, and DAO participation
- **Avatar wearables** showcase your digital journey

## 🏆 Badge Categories

### Skill Badges
Role-based progression system representing competencies:
- **Development**: Frontend, Backend, Smart Contracts, DevOps
- **Community**: Moderation, Translation, Content Creation
- **Business**: Marketing, Legal, Operations, Product

### Achievement Badges
Milestone-based collectibles earned through:
- **Platform Achievements**: GitHub contributions, Discord activity
- **Community Participation**: DAO governance, event attendance
- **Special Events**: Hackathons, launches, collaborations

### Procedural Badges
Unique, soulbound items generated from your digital identity:
- **Keyblade Weapons**: Generated from wallet addresses
- **Loot Equipment**: Based on contribution history
- **POAP Wearables**: Attendance proofs as 3D badges

## 🎯 Character Studio Integration

**Character Studio is now fully on-chain on Solana** - a trustless, decentralized system for badge claiming and avatar customization.

### 🔓 On-Chain Badge System
- **No Servers Required**: Everything managed via Program Derived Accounts (PDAs)
- **Dual Unlock Methods**: Purchase with SPL tokens OR claim with achievement passwords
- **Creator Control**: Badge creators set prices, unlock conditions, and claimable criteria
- **User Ownership**: All badge ownership stored on-chain as bitmasks

### 🛠️ How It Works

1. **Connect Wallet** - Access your on-chain badge collection
2. **Purchase Badges** - Buy directly with SOL/USDC/SPL tokens
3. **Claim Achievements** - Unlock badges with password verification for earned accomplishments
4. **Customize Avatar** - Drag and drop owned badges onto your character
5. **Export & Share** - Use your avatar across metaverse platforms

### 🔐 Achievement Claiming Flow

```rust
// Badge creators define unlock conditions
CollectionPricesData {
    claimables: Vec<u8>,           // Achievement-based badges
    purchasables: Vec<u8>,         // Buyable cosmetic badges  
    unlock_password_hash: [u8; 32], // SHA-256 of achievement password
    prices: Vec<u64>,              // Prices for purchasable badges
}
```

**Example Achievement Flow:**
1. Complete GitHub milestone → Receive unlock password
2. Enter password in Character Studio
3. SHA-256 verification unlocks dev badge on-chain
4. Badge permanently added to your collection PDA

### 🎮 Badge Categories in Character Studio

- **🛒 Purchasable**: Cosmetic badges available for direct purchase
- **🏆 Claimable**: Achievement badges unlocked via verified accomplishments
- **🔓 Hybrid**: Badges that can be both earned through achievements OR purchased

## 🔗 Distribution

- **NFT Collection**: [M3rit on Zora](https://zora.co/collect/oeth:0x1a3a6e18f50fcc943b64d92098e1ca6b9b4d0812)
- **3D Models**: [Sketchfab Collection](https://skfb.ly/oFGqA)
- **Open Source**: Free download from GitHub for community use

## 🚀 Getting Started

### For Developers
```bash
# Convert SVG logos to 3D badges
blender -b logo-generator/logo_automate.blend --python logo-generator/svg_to_glb.py -- -i logo.svg -o badge.glb
```

### For Communities
1. **Design Achievement Criteria** - Define what earns each badge
2. **Create Badge Assets** - Use our templates or design custom ones
3. **Integrate with Character Studio** - Enable automatic badge claiming
4. **Set Up Distribution** - Mint badges for community members

## 🛠️ Technical Stack

### 3D Asset Pipeline
- **Blender**: Geometry nodes for procedural badge generation
- **Formats**: GLB (web), FBX (games), VRM (avatars)
- **Automation**: Python scripts for SVG → 3D conversion
- **Templates**: Master .blend files for consistent styling

### On-Chain Infrastructure (Solana)
- **Program Derived Accounts (PDAs)**: Trustless badge ownership storage
- **Bitmask Storage**: Efficient on-chain trait ownership tracking
- **SHA-256 Verification**: Password-based achievement unlocking
- **SPL Token Support**: SOL, USDC, and custom token payments
- **No Backend Required**: Fully decentralized validation

### Integration Ecosystem
- **Character Studio**: Avatar customization and badge claiming interface
- **Collection Creator App**: Tools for badge creators to set prices and unlock conditions
- **Achievement Tracking**: Integration with GitHub, Discord, Dework for automated unlocks

## 🎨 Contributing

Looking for badge designs representing various achievements, roles, and skills!

- **Propose Ideas**: Open an issue with achievement concepts
- **Submit Designs**: Create badges following our design guidelines
- **Integrate Platforms**: Help connect new achievement sources
- **Build Tools**: Improve the badge creation pipeline

## 🌐 Related Projects

- **[Character Studio](https://github.com/M3-org/CharacterStudio)** - On-chain avatar creation and badge claiming interface
- **[Collection Prices App](https://github.com/memelotsqui/Collection_Prices)** - Solana PDA management for creators
- **[ElizaOS Analytics](https://github.com/elizaOS/elizaos.github.io)** - GitHub-based reputation tracking
- **[Loot Assets](https://github.com/m3-org/loot-assets)** - 3D equipment and wearables
- **[Character Assets](https://github.com/memelotsqui/character-assets)** - Sample asset packs for Character Studio

## 🚧 Development Status

**Character Studio On-Chain Integration:**
- ✅ PDA-based badge ownership system
- ✅ Dual purchase/claim unlock methods  
- ✅ SHA-256 password verification
- ✅ Collection Creator management tools
- 🚧 URI metadata expansion
- 🚧 Enhanced password unlock frontend
- 🚧 Creator dashboard improvements

**Contributing to the ecosystem:**
- 💡 **Propose achievements** for new badge types
- 🎨 **Design badges** following our templates
- 🔧 **Build integrations** with platforms and tools
- 📝 **Contribute documentation** and tutorials

---

*Building the reputation layer for the internet, one badge at a time.*
