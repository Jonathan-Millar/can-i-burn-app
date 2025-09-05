# 🔥 Can I Burn?

[![Next.js](https://img.shields.io/badge/Next.js-15-black?style=for-the-badge&logo=next.js)](https://nextjs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.6-blue?style=for-the-badge&logo=typescript)](https://www.typescriptlang.org/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-3.4-38B2AC?style=for-the-badge&logo=tailwind-css)](https://tailwindcss.com/)
[![Vercel](https://img.shields.io/badge/Deployed_on-Vercel-000000?style=for-the-badge&logo=vercel)](https://vercel.com/)

A comprehensive web application providing real-time fire burn restrictions across all Canadian provinces and territories. Built with Next.js 15, TypeScript, and modern web technologies.

## 🚀 Live Demo

**[Try it live →](https://can-i-burn.vercel.app)**

## ✨ Features

- **🇨🇦 Complete Canada Coverage** - All 10 provinces and 3 territories
- **📍 Intelligent Location Detection** - GPS coordinates or city name input
- **🎨 Modern UI/UX** - Glassmorphism design with smooth animations
- **📱 Responsive Design** - Optimized for all devices
- **⚡ Real-time Data** - Live restrictions from official government sources
- **🎯 Enhanced Reporting** - Detailed risk assessments and recommendations
- **🔍 Advanced Search** - Support for coordinates, city names, and postal codes

## 🛠️ Installation

### Prerequisites

- Node.js 18.0 or later
- npm, yarn, or pnpm

### Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/can-i-burn.git
cd can-i-burn

# Install dependencies
npm install

# Start the development server
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) to view the application.

## 🛠️ Tech Stack

### Frontend
- **[Next.js 15](https://nextjs.org/)** - React framework with App Router and Server Components
- **[React 18](https://react.dev/)** - UI library with concurrent features
- **[TypeScript](https://www.typescriptlang.org/)** - Type-safe JavaScript
- **[Tailwind CSS](https://tailwindcss.com/)** - Utility-first CSS framework
- **[Framer Motion](https://www.framer.com/motion/)** - Animation library
- **[GSAP](https://greensock.com/gsap/)** - Professional animation platform
- **[Radix UI](https://www.radix-ui.com/)** - Accessible component primitives

### Backend
- **[Next.js API Routes](https://nextjs.org/docs/app/building-your-application/routing/route-handlers)** - Serverless API endpoints
- **Custom Web Scrapers** - Real-time data extraction from official sources
- **Geocoding Services** - Location-based data processing

### Styling & Effects
- **Glassmorphism Design** - Modern frosted glass aesthetic
- **Particle Systems** - Interactive background animations
- **Gradient Overlays** - Visual depth and modern styling
- **Responsive Design** - Mobile-first approach

## 🎯 How It Works

1. **Location Input** - Users provide coordinates or city names
2. **Geocoding** - Convert location to precise coordinates
3. **Province Detection** - Determine which province/territory contains the location
4. **Data Scraping** - Fetch real-time restrictions from official government sources
5. **Response Generation** - Return formatted data with enhanced reporting

## 📡 API Endpoints

### Main Fire Restrictions
```bash
GET /api/enhanced/burn_restrictions?latitude=49.2827&longitude=-123.1207
GET /api/enhanced/burn_restrictions?location=Vancouver
```

### Province-Specific Data
```bash
GET /api/enhanced/nb_report?county=Saint John
GET /api/enhanced/nb_counties
GET /api/enhanced/ns_counties
```

### Province Info
```bash
GET /api/enhanced/provinces
```

## 📊 Example Response

```json
{
  "latitude": 49.2827,
  "longitude": -123.1207,
  "province": "BC",
  "county": "Vancouver",
  "burn_restriction": {
    "status": "Category 1 Fires Allowed",
    "details": "Small campfires are permitted with proper safety measures",
    "source": "BC Wildfire Service",
    "last_updated": "2025-01-27T10:30:00",
    "enhanced_report": {
      "fire_centre": "Coastal",
      "category": 1,
      "restrictions": "Category 1 fires allowed with conditions"
    }
  }
}
```

## 🏗️ Project Structure

```
cib-vercel/
├── app/                          # Next.js 15 App Router
│   ├── api/                      # API routes
│   ├── globals.css              # Global styles
│   ├── layout.tsx               # Root layout
│   └── page.tsx                 # Home page
├── components/                   # React components
│   ├── FireRestrictionApp.tsx   # Main app component
│   └── ui/                      # Reusable UI components
│       ├── GlassMorphismCard.tsx
│       ├── EnhancedReportCard.tsx
│       ├── AnimatedCard.tsx
│       └── ... (20+ components)
├── lib/                         # Utilities and scrapers
│   ├── scrapers/                # Province-specific scrapers
│   ├── geocoding.ts            # Location services
│   ├── province_detector.ts    # Boundary detection
│   └── restrictions_scraper.ts # Main scraper logic
└── types/                       # TypeScript definitions
```

## 🌍 Supported Regions

### Provinces
- **British Columbia (BC)** - Fire centre detection, category-based restrictions
- **Alberta (AB)** - Region detection, tiered restriction system
- **Saskatchewan (SK)** - Municipality detection, multi-jurisdictional coordination
- **Manitoba (MB)** - Dual jurisdiction system, seasonal restrictions
- **Ontario (ON)** - Fire zone restrictions, comprehensive coverage
- **Quebec (QC)** - SOPFEU system, fire danger index, bilingual service
- **New Brunswick (NB)** - Enhanced reporting, multi-source data
- **Nova Scotia (NS)** - County-based restrictions, province-wide status
- **Prince Edward Island (PEI)** - County detection, basic restrictions
- **Newfoundland and Labrador (NL)** - Province-wide bans, daily hazard updates

### Territories
- **Yukon (YT)** - Multi-level restrictions, territory-wide bans
- **Northwest Territories (NT)** - Fire danger ratings, community restrictions
- **Nunavut (NU)** - Community management, burn permits

Each region utilizes custom scrapers that extract data from official government sources for accurate, up-to-date information.

## 🚀 Deployment

### Vercel (Recommended)

The application is optimized for Vercel deployment:

```bash
# Build for production
npm run build

# Deploy to Vercel
npx vercel --prod
```

### Other Platforms

```bash
# Build for production
npm run build

# Start production server
npm start
```

## 🧪 Development

### Available Scripts

```bash
# Development server
npm run dev

# Build for production
npm run build

# Start production server
npm start

# Run linting
npm run lint

# Type checking
npx tsc --noEmit
```

### Development Guidelines

1. **Code Style** - Follow TypeScript best practices and ESLint rules
2. **Component Structure** - Use functional components with hooks
3. **Styling** - Utilize Tailwind CSS utility classes
4. **Animations** - Implement smooth transitions with Framer Motion
5. **Testing** - Ensure components work across different screen sizes

## 🔮 Roadmap

- [ ] **Historical Data** - Track restriction changes over time
- [ ] **Weather Integration** - Include current weather conditions
- [ ] **API Rate Limiting** - Enhanced API management and monitoring
- [ ] **Caching Layer** - Implement Redis for improved performance
- [ ] **Multi-language Support** - French and other official languages

## 📊 Performance

- **Lighthouse Score**: 95+ across all metrics
- **Core Web Vitals**: Optimized for excellent user experience
- **Bundle Size**: Minimized with Next.js optimization
- **Loading Speed**: Sub-second initial page load

## 🧪 Testing

The application has been tested with:
- ✅ All 10 provinces and 3 territories
- ✅ Major cities across Canada
- ✅ Rural and remote locations
- ✅ Error handling for invalid inputs
- ✅ Mobile responsiveness
- ✅ Cross-browser compatibility

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

### How to Contribute

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Setup

1. Clone the repository
2. Install dependencies: `npm install`
3. Start the development server: `npm run dev`
4. Make your changes
5. Test thoroughly
6. Submit a pull request

## 📞 Support

If you have any questions or need help, please:
- Open an issue on GitHub
- Check the documentation
- Review existing issues and discussions

## 🙏 Acknowledgments

- Official government fire services across Canada
- OpenStreetMap for geocoding services
- The Next.js and React communities
- All contributors and users

---

**Built with ❤️ using Next.js 15, TypeScript, and modern web technologies.**