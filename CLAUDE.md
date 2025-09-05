# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

### Frontend (Next.js) - Primary Implementation
- **Development**: `npm run dev` (runs on port 3000)
- **Build**: `npm run build`
- **Production**: `npm run start`
- **Lint**: `npm run lint`
- **Install dependencies**: `npm install`

## Architecture Overview

This is a modern Next.js web application providing Canada-wide fire burn restriction information using TypeScript and shadcn/ui components.

### Current Architecture (Next.js 14)
- **Framework**: Next.js 14 with App Router and TypeScript
- **UI**: shadcn/ui components with Tailwind CSS and Framer Motion animations
- **Entry point**: `app/page.tsx` - main application interface
- **API Routes**: Server-side API endpoints in `app/api/`
- **Components**: Located in `components/ui/` (shadcn components)
- **Styling**: Tailwind CSS with custom design system and glassmorphism effects
- **Data Fetching**: Modern fetch-based scrapers with proper error handling

### Core Modules

#### Province Detection System
- **Core module**: `lib/province_detector.ts`
- **Geocoding**: Nominatim integration for location name to coordinate conversion
- **Coverage**: All 10 provinces and 3 territories
- **Real-time coordinate-to-province/county mapping**

#### Fire Restriction Scrapers
Modular TypeScript scraper system for real-time data from official sources:
- **Main coordinator**: `lib/restrictions_scraper.ts`
- **Province-specific scrapers**: `lib/scrapers/[province]_scraper.ts`
  - `nb_scraper.ts`: Enhanced New Brunswick scraper with county-specific data
  - `ns_scraper.ts`: Nova Scotia scraper
  - `ontario_scraper.ts`: Ontario scraper
  - `bc_scraper.ts`: British Columbia scraper
  - `alberta_scraper.ts`: Alberta scraper
  - `saskatchewan_scraper.ts`: Saskatchewan scraper
  - `manitoba_scraper.ts`: Manitoba scraper
  - `quebec_scraper.ts`: Quebec scraper
  - `newfoundland_scraper.ts`: Newfoundland scraper
  - `territories_scraper.ts`: YT, NT, NU scraper
  - `pei_scraper.ts`: Prince Edward Island scraper
- **Data sources**: Official provincial/territorial fire services and government APIs

### API Architecture
- **Enhanced endpoints**: `app/api/enhanced/burn_restrictions/route.ts` (Canada-wide)
- **Next.js API Routes**: Server-side processing with TypeScript
- **Real-time data**: Direct scraping from provincial sources

### Key Features
- **Glassmorphism UI**: Modern glass-effect design with backdrop blur
- **Animated Components**: Smooth transitions with Framer Motion
- **Responsive Design**: Mobile-first approach with Tailwind CSS
- **Real-time Data**: Live fire restriction updates from official sources
- **Advanced Search**: Location-based and coordinate-based lookups
- **Province Coverage**: All 10 provinces and 3 territories supported

## Key Development Patterns

### Adding New Province/Territory Support
1. Create scraper in `lib/scrapers/[province]_scraper.ts`
2. Add import and case in `lib/restrictions_scraper.ts`
3. Update province detection logic in `lib/province_detector.ts` if required
4. Test with real coordinates from that province

### API Response Format
Standard response structure across all endpoints:
```typescript
{
    "latitude": number,
    "longitude": number,
    "province": string,
    "county": string | null,
    "burn_status": "no fires" | "restricted burning" | "open burning",
    "location": string,
    "details": string[],
    "validity_period_start": string,
    "validity_period_end": string,
    "source": string,
    "last_updated": string,
    "enhanced_report": object // Optional
}
```

### Error Handling
- Geocoding failures return specific error messages
- Invalid coordinates handled gracefully
- Province detection failures provide fallback responses
- Scraping failures fall back to generic province-wide status

### Rate Limiting
- Nominatim geocoding includes respectful rate limiting with exponential backoff
- Multiple retry attempts with delay
- User-Agent headers for API compliance

## Environment Configuration

### Environment Variables
- **Frontend**: `.env.local` (optional for local development)
- **Production**: Vercel environment variables for deployment

### Dependencies
- **Runtime**: Next.js 14, React 18, TypeScript 5.6
- **UI**: shadcn/ui, Tailwind CSS, Framer Motion
- **Utilities**: Radix UI primitives, class-variance-authority, clsx
- **Data Fetching**: Native fetch API with proper error handling

## Testing Strategy

Currently no automated tests are present. For testing:
- Manual testing covers all provinces/territories
- Test major cities and rural locations
- Verify error handling for invalid inputs
- Test mobile responsiveness
- Test API endpoints directly

## File Structure

```
pei_fire_watch/
├── app/                              # Next.js App Router
│   ├── api/enhanced/burn_restrictions/ # API endpoint
│   ├── layout.tsx                    # Root layout
│   └── page.tsx                      # Main page
├── components/                       # React components
│   ├── FireRestrictionApp.tsx       # Main app component
│   └── ui/                          # shadcn/ui components
├── lib/                             # Core business logic
│   ├── province_detector.ts         # Province/county detection
│   ├── restrictions_scraper.ts      # Main scraper coordinator
│   ├── geocoding.ts                 # Location geocoding
│   └── scrapers/                    # Province-specific scrapers
│       ├── nb_scraper.ts           # New Brunswick (enhanced)
│       ├── ns_scraper.ts           # Nova Scotia
│       ├── ontario_scraper.ts      # Ontario
│       ├── bc_scraper.ts           # British Columbia
│       ├── alberta_scraper.ts      # Alberta
│       ├── saskatchewan_scraper.ts # Saskatchewan
│       ├── manitoba_scraper.ts     # Manitoba
│       ├── quebec_scraper.ts       # Quebec
│       ├── newfoundland_scraper.ts # Newfoundland
│       ├── territories_scraper.ts  # YT, NT, NU
│       └── pei_scraper.ts          # Prince Edward Island
├── package.json                     # Dependencies and scripts
├── tailwind.config.js              # Tailwind configuration
└── tsconfig.json                   # TypeScript configuration
```
