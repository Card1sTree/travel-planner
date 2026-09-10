# Product Build Plan

This document tracks the product work separately from the deployment platform. The goal is to turn the original API demo into a useful travel-planning product before choosing the final hosting stack.

## Product direction

Roam is a travel planning workspace that turns a travel mood, time window, and budget into a considered itinerary. The product should feel calm and editorial rather than like an administration dashboard.

## Step 1: Establish the web product shell

Status: Complete

- Added a `web/` Next.js application using TypeScript, App Router, Tailwind CSS, and npm.
- Added `lucide-react` for accessible interface icons.
- Replaced the starter screen with the Roam travel-planning experience.
- Added responsive navigation, trip planning inputs, travel mood selection, destination inspiration, and itinerary preview.
- Added demo-mode behavior so the interface remains usable while backend services are unavailable.
- Added `NEXT_PUBLIC_TRIP_PLANNER_URL` as the integration boundary for the Trip Planner API.

Validation completed:

- `npm run lint`
- `npm run build`
- Browser check at desktop and mobile sizes
- Mobile navigation interaction check

## Step 2: Connect the real API

Status: Next

- Add a development environment file with the Trip Planner API URL.
- Add CORS configuration to the FastAPI service.
- Map the returned TripPlan into the itinerary component.
- Replace the demo Paris result after a successful API response.
- Add clear loading, empty, and error states.

## Step 3: Make trip planning persistent

Status: Planned

- Replace in-memory users and trips with PostgreSQL repositories.
- Add database migrations.
- Add stable user and trip identifiers.
- Add saved itinerary retrieval and deletion.

## Step 4: Add product essentials

Status: Planned

- Authentication and user accounts.
- Saved destinations and trip history.
- Editable itinerary days.
- Budget breakdown and currency handling.
- Travel preferences and accessibility options.
- Shareable itinerary links.

## Step 5: Improve recommendations

Status: Planned

- Expose model version and confidence metadata.
- Add recommendation explanations based on actual model features.
- Add model evaluation thresholds.
- Add feedback from saved or rejected recommendations.
- Track experiments separately from the application runtime.

## Step 6: Prepare the user-facing release

Status: Planned

- Add frontend tests and API contract tests.
- Add accessibility checks.
- Add product analytics with privacy-respecting events.
- Add error tracking and request tracing.
- Add a production Docker image for the web application.
- Choose hosting after the product workflow is stable.

## Current architecture

```text
Next.js web app
       |
       v
FastAPI Trip Planner ----> Recommendation Engine
       |
       v
   PostgreSQL
```

The Python services remain in place because Python is appropriate for the API and machine-learning workloads. The modern product layer is the typed Next.js frontend.
