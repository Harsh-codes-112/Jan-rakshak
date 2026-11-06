import React from 'react';
import { Shield, FileText, AlertTriangle, MapPin } from "lucide-react";

export default function CitizenDashboard() {
  return (
    <div className="min-h-screen bg-slate-50 font-sans">
      <header className="bg-[#0f172a] text-white p-4 shadow-md border-b-4 border-[#ff9933]">
        <div className="container mx-auto flex justify-between items-center">
          <h1 className="text-2xl font-bold tracking-tight">JAN-RAKSHAK</h1>
          <nav className="space-x-4 flex">
            <button className="px-4 py-2 hover:bg-slate-800 rounded">My Profile</button>
            <button className="px-4 py-2 bg-red-600 hover:bg-red-700 rounded flex items-center">
              <AlertTriangle className="mr-2 h-4 w-4" /> Emergency SOS
            </button>
          </nav>
        </div>
      </header>

      <div className="bg-white py-12 text-center border-b">
        <h2 className="text-3xl font-extrabold text-[#0f172a]">Your Voice. Your Evidence. Your Rights.</h2>
        <p className="text-slate-600 mt-2 max-w-2xl mx-auto">
          Securely report corruption, track grievances, and access AI-assisted legal intelligence based on Bharatiya Nyaya Sanhita (BNS).
        </p>
      </div>

      <main className="container mx-auto p-6 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mt-6">
        <div className="bg-white p-6 rounded-lg shadow border-l-4 border-[#0f172a]">
          <Shield className="h-8 w-8 text-[#0f172a] mb-2" />
          <h3 className="text-lg font-bold mb-2">Report Corruption</h3>
          <p className="text-sm text-slate-500 mb-4">Submit an encrypted report with photo, video, or audio evidence.</p>
          <button className="w-full bg-[#0f172a] text-white py-2 rounded">Start Report</button>
        </div>

        <div className="bg-white p-6 rounded-lg shadow border-l-4 border-blue-500">
          <FileText className="h-8 w-8 text-blue-500 mb-2" />
          <h3 className="text-lg font-bold mb-2">Legal Assistance</h3>
          <p className="text-sm text-slate-500 mb-4">Chat with our RAG AI to understand applicable laws and draft formats.</p>
          <button className="w-full border border-slate-300 py-2 rounded hover:bg-slate-50">Open AI Assistant</button>
        </div>

        <div className="bg-white p-6 rounded-lg shadow border-l-4 border-green-500">
          <MapPin className="h-8 w-8 text-green-500 mb-2" />
          <h3 className="text-lg font-bold mb-2">Civic Issue Map</h3>
          <p className="text-sm text-slate-500 mb-4">View anonymized, aggregated civic grievances in your locality.</p>
          <button className="w-full border border-slate-300 py-2 rounded hover:bg-slate-50">View Map</button>
        </div>
      </main>
    </div>
  );
}
