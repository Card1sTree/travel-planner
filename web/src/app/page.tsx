"use client";

import {
  ArrowUpRight,
  CalendarDays,
  Check,
  ChevronDown,
  Compass,
  MapPin,
  Menu,
  Plane,
  Search,
  Sparkles,
  WalletCards,
  X,
} from "lucide-react";
import { FormEvent, useState } from "react";

type ItineraryDay = {
  day: string;
  title: string;
  description: string;
  tag: string;
};

const moods = [
  { value: "Rest & reset", color: "sage" },
  { value: "Food & culture", color: "coral" },
  { value: "Nature & adventure", color: "ochre" },
];

const demoItinerary: ItineraryDay[] = [
  { day: "01", title: "Arrive with room to wander", description: "Settle into Le Marais, then follow the river lights toward a small bistro dinner.", tag: "Easy pace" },
  { day: "02", title: "The city, at street level", description: "A market breakfast, hidden courtyards, and a self-guided walk through Montmartre.", tag: "Neighborhoods" },
  { day: "03", title: "Art, then an aperitif", description: "Spend the afternoon with the classics before finding a sunny terrace for golden hour.", tag: "Culture" },
];

export default function Home() {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [destination, setDestination] = useState("");
  const [mood, setMood] = useState("Food & culture");
  const [budget, setBudget] = useState("2500");
  const [isPlanning, setIsPlanning] = useState(false);
  const [hasPlanned, setHasPlanned] = useState(false);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setIsPlanning(true);
    const apiUrl = process.env.NEXT_PUBLIC_TRIP_PLANNER_URL;
    if (apiUrl) {
      try {
        await fetch(`${apiUrl}/trips`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ user_id: "demo_user", start_date: "2026-06-12", end_date: "2026-06-15", budget: Number(budget), preferred_activity: mood }),
        });
      } catch {
        // Keep the demo itinerary available while the API is unavailable.
      }
    }
    window.setTimeout(() => {
      setIsPlanning(false);
      setHasPlanned(true);
      document.getElementById("itinerary")?.scrollIntoView({ behavior: "smooth" });
    }, 650);
  }

  return (
    <main className="app-shell">
      <nav className="topbar" aria-label="Main navigation">
        <a className="brand" href="#top" aria-label="Roam home"><span className="brand-mark"><Compass size={19} strokeWidth={2.5} /></span><span>roam</span></a>
        <div className={`nav-links ${isMenuOpen ? "nav-links-open" : ""}`}>
          <a href="#planner" onClick={() => setIsMenuOpen(false)}>Plan a trip</a>
          <a href="#inspiration" onClick={() => setIsMenuOpen(false)}>Inspiration</a>
          <a href="#itinerary" onClick={() => setIsMenuOpen(false)}>My itineraries</a>
          <button className="mobile-close" onClick={() => setIsMenuOpen(false)} aria-label="Close menu"><X size={20} /></button>
        </div>
        <div className="nav-actions"><button className="text-button">Sign in</button><button className="avatar-button" aria-label="Open profile">AM</button></div>
        <button className="menu-button" onClick={() => setIsMenuOpen(true)} aria-label="Open menu"><Menu size={22} /></button>
      </nav>

      <section className="hero" id="top">
        <div className="hero-copy"><p className="eyebrow"><Sparkles size={15} /> Travel, thoughtfully planned</p><h1>Go somewhere<br /><em>that feels like you.</em></h1><p className="hero-description">Roam turns the feeling you&apos;re chasing into a trip worth remembering. Less tab switching. More looking forward to it.</p><a className="hero-link" href="#planner">Start planning <ArrowUpRight size={17} /></a></div>
        <div className="hero-art" aria-label="A sunny Mediterranean travel scene"><div className="sun" /><div className="arch arch-back" /><div className="arch arch-front" /><div className="hill hill-one" /><div className="hill hill-two" /><div className="hero-stamp"><span>Field notes</span><strong>06 / 26</strong></div></div>
      </section>

      <section className="planner-section" id="planner">
        <div className="section-heading"><div><p className="eyebrow">Your next chapter</p><h2>Let&apos;s make a plan.</h2></div><p className="section-note">Tell us the shape of your trip. We&apos;ll fill in the good parts.</p></div>
        <form className="planner-form" onSubmit={handleSubmit}>
          <label className="field field-destination"><span>Where are you dreaming of?</span><div className="input-wrap"><Search size={18} /><input value={destination} onChange={(event) => setDestination(event.target.value)} placeholder="Anywhere, really..." /></div></label>
          <label className="field"><span>When</span><div className="input-wrap"><CalendarDays size={18} /><select defaultValue="June 12 — June 15"><option>June 12 — June 15</option><option>July 03 — July 09</option><option>September 18 — September 23</option></select><ChevronDown className="select-icon" size={16} /></div></label>
          <label className="field"><span>Budget</span><div className="input-wrap"><WalletCards size={18} /><span className="currency">$</span><input type="number" min="500" value={budget} onChange={(event) => setBudget(event.target.value)} /><span className="muted">total</span></div></label>
          <button className="primary-button" type="submit" disabled={isPlanning}>{isPlanning ? "Finding your way..." : "Build my trip"}<ArrowUpRight size={18} /></button>
        </form>
        <div className="mood-row" aria-label="Choose a travel mood"><span className="mood-label">I&apos;m craving</span>{moods.map((item) => <button type="button" key={item.value} className={`mood-chip ${mood === item.value ? "selected" : ""} ${item.color}`} onClick={() => setMood(item.value)}><span className="chip-dot" />{item.value}</button>)}</div>
      </section>

      <section className="inspiration-section" id="inspiration"><div className="section-heading compact"><div><p className="eyebrow">A little nudge</p><h2>Places with a point of view.</h2></div><a className="underlined-link" href="#planner">See all inspiration <ArrowUpRight size={16} /></a></div><div className="destination-grid"><article className="destination-card card-coast"><div className="card-sun" /><div className="destination-content"><span>01 / Coastline</span><h3>Menorca, Spain</h3><p>Salt air, quiet coves, long lunches.</p></div></article><article className="destination-card card-city"><div className="city-skyline"><span /><span /><span /><span /></div><div className="destination-content"><span>02 / City rhythm</span><h3>Kyoto, Japan</h3><p>Temple gardens, tiny bars, deep craft.</p></div></article><article className="destination-card card-highland"><div className="highland-sun" /><div className="destination-content"><span>03 / Wide open</span><h3>Highlands, Scotland</h3><p>Misty trails and fireside stories.</p></div></article></div></section>

      <section className={`itinerary-section ${hasPlanned ? "itinerary-visible" : ""}`} id="itinerary"><div className="itinerary-intro"><p className="eyebrow"><MapPin size={15} /> Your trip preview</p><h2>Paris, in your own rhythm.</h2><p>Three days shaped around {mood.toLowerCase()}, with enough white space for the unexpected.</p><button className="secondary-button" type="button"><Plane size={17} /> Save itinerary</button></div><div className="itinerary-list">{demoItinerary.map((item) => <article className="itinerary-item" key={item.day}><span className="day-number">{item.day}</span><div><span className="item-tag">{item.tag}</span><h3>{item.title}</h3><p>{item.description}</p></div><span className="check-circle"><Check size={15} /></span></article>)}</div></section>

      <footer className="footer"><div className="brand"><span className="brand-mark"><Compass size={17} /></span><span>roam</span></div><p>Made for the curious.</p><span>© 2026 Roam Travel Co.</span></footer>
    </main>
  );
}
