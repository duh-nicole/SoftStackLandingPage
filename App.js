import React from 'react';

export default function App() {
    return (
        <div className="min-h-screen bg-[#d9f2ff] text-[#77529e] selection:bg-[#dcb5ff] selection:text-[#77529e]">

            {/* ☰ Navigation */}
            <nav className="sticky top-0 z-50 border-b-4 border-[#77529e] bg-[#77529e] px-4 py-3 text-[#d9f2ff]">
                <div className="mx-auto flex max-w-6xl items-center justify-between font-mono">
                    <div className="flex items-center gap-2 text-lg font-bold tracking-wider">
                        <span>☕</span>
                        <span>CAFE_OS.SYS</span>
                    </div>
                    <div className="hidden gap-6 text-sm md:flex">
                        <a href="#features" className="hover:underline">//_features</a>
                        <a href="#onboard" className="hover:underline">//_join</a>
                    </div>
                    <a
                        href="#onboard"
                        className="border-2 border-[#d9f2ff] bg-[#dcb5ff] px-3 py-1 text-xs font-bold text-[#77529e] shadow-[2px_2px_0px_0px_rgba(217,242,255,1)] transition-all hover:translate-x-[2px] hover:translate-y-[2px] hover:shadow-none"
                    >
                        LAUNCH.EXE
                    </a>
                </div>
            </nav>

            {/* 🚀 Hero Section */}
            <header className="mx-auto max-w-4xl px-4 py-16 text-center md:py-24">
                <div
                    className="inline-block border-2 border-[#77529e] bg-[#dcb5ff] px-3 py-1 text-xs font-mono font-bold tracking-widest text-[#77529e] uppercase shadow-[4px_4px_0px_0px_#77529e] mb-6">
                    v1.0.0 Stable Build
                </div>
                <h1 className="font-mono text-4xl font-extrabold tracking-tight md:text-6xl uppercase">
                    Cozy Vibes. <br/>
                    <span className="text-white drop-shadow-[2px_2px_0px_#77529e]">Smart Inventory.</span>
                </h1>
                <p className="mx-auto mt-6 max-w-xl text-lg font-medium leading-relaxed">
                    A retro-inspired management deck built to breathe fresh life into your stock before it turns cold.
                    Track everything through a beautifully simple pixel-perfect view.
                </p>
                <div className="mt-10 flex justify-center">
                    <a
                        href="#onboard"
                        className="border-4 border-[#77529e] bg-[#a5bdfd] px-8 py-3 font-mono font-bold text-[#77529e] shadow-[4px_4px_0px_0px_#77529e] transition-all hover:translate-x-[4px] hover:translate-y-[4px] hover:shadow-none text-lg"
                    >
                        SYS_INIT()
                    </a>
                </div>
            </header>

            {/* ⭐ Features Grid */}
            <section id="features" className="mx-auto max-w-6xl px-4 py-12 border-t-4 border-dashed border-[#77529e]">
                <h2 className="text-center font-mono text-2xl font-bold uppercase tracking-wider mb-12">//
                    core_modules</h2>
                <div className="grid gap-6 md:grid-cols-3">

                    {/* Card 1 */}
                    <div className="border-4 border-[#77529e] bg-white p-6 shadow-[4px_4px_0px_0px_#77529e]">
                        <div className="text-3xl mb-4">💾</div>
                        <h3 className="font-mono font-bold text-lg uppercase mb-2">Automated Audit</h3>
                        <p className="text-sm leading-relaxed text-gray-700">Never let products collect digital dust.
                            Run lightning-fast diagnostic logs on slow-moving inventory items.</p>
                    </div>

                    {/* Card 2 */}
                    <div className="border-4 border-[#77529e] bg-white p-6 shadow-[4px_4px_0px_0px_#77529e]">
                        <div className="text-3xl mb-4">📟</div>
                        <h3 className="font-mono font-bold text-lg uppercase mb-2">Responsive OS</h3>
                        <p className="text-sm leading-relaxed text-gray-700">Perfectly scaling view systems custom
                            fitted to any resolution window, from massive modern rigs to handheld pocket devices.</p>
                    </div>

                    {/* Card 3 */}
                    <div className="border-4 border-[#77529e] bg-white p-6 shadow-[4px_4px_0px_0px_#77529e]">
                        <div className="text-3xl mb-4">🔌</div>
                        <h3 className="font-mono font-bold text-lg uppercase mb-2">Clean Pipeline</h3>
                        <p className="text-sm leading-relaxed text-gray-700">Sanitized, encrypted data pathways
                            structured to hook cleanly into high-performance backend layers or local storage stacks.</p>
                    </div>

                </div>
            </section>

            {/* 📣 CTA Onboarding Form Banner */}
            <section id="onboard" className="bg-[#77529e] py-16 text-[#d9f2ff] border-t-4 border-[#77529e]">
                <div className="mx-auto max-w-md px-4">

                    {/* Desktop App Style Window Container */}
                    <div
                        className="border-4 border-white bg-[#d9f2ff] text-[#77529e] shadow-[8px_8px_0px_0px_rgba(220,181,255,1)]">
                        {/* Window Top Title Bar */}
                        <div
                            className="bg-white border-b-4 border-[#77529e] px-3 py-2 flex justify-between items-center font-mono text-xs font-bold">
                            <span>onboarding_wizard.exe</span>
                            <div className="flex gap-1">
                                <span className="w-2 h-2 border border-[#77529e]"></span>
                                <span className="w-2 h-2 border border-[#77529e] bg-[#77529e]"></span>
                            </div>
                        </div>

                        {/* Form Content configured for Web3Forms */}
                        <form action="https://api.web3forms.com/submit" method="POST" className="p-6 font-mono text-sm">

                            {/* 🔑 Your Live Web3Forms Key */}
                            <input type="hidden" name="access_key" value="53f6faa6-c347-46cd-a7ff-b4cb6defd107"/>

                            {/* Spam Prevention */}
                            <input type="checkbox" name="botcheck" className="hidden" style={{display: 'none'}}/>

                            <p className="mb-6 font-sans text-center text-gray-700 font-medium">
                                Initialize your terminal credentials to get early deployment access.
                            </p>

                            <div className="mb-4">
                                <label className="block font-bold mb-1 uppercase tracking-wide text-xs">User Name
                                    :</label>
                                <input
                                    type="text"
                                    name="name"
                                    required
                                    className="w-full border-2 border-[#77529e] px-3 py-2 text-sm outline-none focus:bg-[#dcb5ff] transition-all bg-white"
                                    placeholder="e.g., duh-nicole"
                                />
                            </div>

                            <div className="mb-6">
                                <label className="block font-bold mb-1 uppercase tracking-wide text-xs">Email Endpoint
                                    :</label>
                                <input
                                    type="email"
                                    name="email"
                                    required
                                    className="w-full border-2 border-[#77529e] px-3 py-2 text-sm outline-none focus:bg-[#dcb5ff] transition-all bg-white"
                                    placeholder="operator@domain.com"
                                />
                            </div>

                            <button
                                type="submit"
                                className="w-full border-2 border-[#77529e] bg-[#77529e] py-2 font-bold text-white uppercase text-xs tracking-widest shadow-[3px_3px_0px_0px_rgba(165,189,253,1)] transition-all hover:translate-x-[2px] hover:translate-y-[2px] hover:shadow-none active:bg-opacity-90"
                            >
                                Execute Submission
                            </button>
                        </form>

                    </div>
                </div>
            </section>

            {/* 📋 Footer */}
            <footer className="border-t-4 border-[#77529e] bg-white py-8 text-center font-mono text-xs">
                <p className="text-gray-500">// CONTROL_BLOCK CLASSIFIED</p>
                <p className="mt-2 font-bold">© 2026 SOFTSTACK STUDIOS. ALL RIGHTS RESERVED.</p>
            </footer>

        </div>
    );
}
