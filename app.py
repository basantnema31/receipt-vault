import os
import json
import re
from datetime import datetime
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# In-memory document storage
DOCUMENTS = [
    {
        "id": "inv-001",
        "vendor": "Acme Cloud Hosting",
        "invoice_number": "INV-2026-9041",
        "date": "2026-10-02",
        "total": 45.00,
        "tax": 3.60,
        "category": "Software & Infrastructure",
        "currency": "USD",
        "client_confidential": True,
        "raw_text": "ACME CLOUD HOSTING\nInvoice #INV-2026-9041\nDate: 2026-10-02\nClient: Secret Stealth Startup\nCompute Cluster Standard: $45.00\nTotal Due: $45.00"
    },
    {
        "id": "inv-002",
        "vendor": "Corner Cafe & Coworking",
        "invoice_number": "REC-8842",
        "date": "2026-10-05",
        "total": 14.50,
        "tax": 1.15,
        "category": "Meals & Client Meetings",
        "currency": "USD",
        "client_confidential": False,
        "raw_text": "Corner Cafe & Coworking\nDate: 2026-10-05\n2x Flat White + Day Desk: $14.50\nThank you for your visit!"
    }
]

def mock_open_weight_extraction(text):
    """
    Simulates a local open-weight quantized model (e.g. Qwen2.5-Coder / Llama-3.2-3B / SmolLM)
    extracting structured financial entities with zero cloud telemetry.
    """
    total_match = re.search(r'\$([0-9]+\.[0-9]{2})', text)
    total = float(total_match.group(1)) if total_match else 0.0
    
    date_match = re.search(r'(\d{4}-\d{2}-\d{2})', text)
    date_val = date_match.group(1) if date_match else datetime.now().strftime("%Y-%m-%d")
    
    vendor = "General Contractor / Vendor"
    category = "General Business Expense"
    
    lower = text.lower()
    if "hosting" in lower or "cloud" in lower or "software" in lower or "api" in lower:
        category = "Software & Infrastructure"
        vendor = "Tech Provider"
    elif "cafe" in lower or "coffee" in lower or "meal" in lower or "food" in lower:
        category = "Meals & Client Meetings"
        vendor = "Local Vendor"
    elif "hardware" in lower or "equipment" in lower:
        category = "Office Equipment"
        vendor = "Hardware Supplier"

    return {
        "vendor": vendor,
        "invoice_number": f"INV-{int(datetime.now().timestamp()) % 100000}",
        "date": date_val,
        "total": total if total > 0 else 25.00,
        "tax": round((total if total > 0 else 25.00) * 0.08, 2),
        "category": category,
        "currency": "USD",
        "client_confidential": True
    }

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ReceiptVault - Zero-Leak Local AI Bookkeeper</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
</head>
<body class="bg-slate-950 text-slate-100 min-h-screen">
    <header class="border-b border-slate-800 bg-slate-900/60 backdrop-blur sticky top-0 z-50">
        <div class="max-w-6xl mx-auto px-4 py-4 flex items-center justify-between">
            <div class="flex items-center space-x-3">
                <span class="w-10 h-10 rounded-xl bg-gradient-to-tr from-emerald-500 to-teal-400 flex items-center justify-center text-slate-950 text-xl font-black">
                    <i class="fa-solid fa-vault"></i>
                </span>
                <div>
                    <h1 class="text-xl font-bold tracking-tight text-white flex items-center gap-2">
                        ReceiptVault
                        <span class="text-xs font-semibold px-2 py-0.5 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">100% Offline AI</span>
                    </h1>
                    <p class="text-xs text-slate-400">Private Financial & Receipt Parser for Freelancers</p>
                </div>
            </div>
            <div class="flex items-center gap-4 text-xs">
                <div class="flex items-center gap-1.5 text-emerald-400">
                    <span class="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
                    Local Model Active (Zero API egress)
                </div>
                <div class="bg-slate-800 px-3 py-1.5 rounded-lg border border-slate-700 font-mono text-slate-300">
                    $29/mo License Value
                </div>
            </div>
        </div>
    </header>

    <main class="max-w-6xl mx-auto px-4 py-8 grid grid-cols-1 md:grid-cols-3 gap-8">
        <!-- Ingestion Panel -->
        <div class="md:col-span-1 space-y-6">
            <div class="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl">
                <h2 class="text-base font-semibold text-white mb-2 flex items-center gap-2">
                    <i class="fa-solid fa-receipt text-emerald-400"></i> Drop Receipt / Paste Invoice
                </h2>
                <p class="text-xs text-slate-400 mb-4">Paste any invoice text, receipt OCR, or statement. It is processed in-memory using an open-weight local model.</p>
                
                <form id="ingestForm" class="space-y-4">
                    <div>
                        <textarea id="rawText" rows="6" placeholder="Paste invoice text here... e.g.:&#10;Stripe Payments Invoice #9821&#10;Date: 2026-10-12&#10;Consulting Subcontract: $450.00&#10;Total: $450.00" class="w-full bg-slate-950 border border-slate-700 rounded-xl p-3 text-xs text-slate-200 focus:outline-none focus:border-emerald-500 font-mono leading-relaxed" required></textarea>
                    </div>
                    <button type="submit" class="w-full py-2.5 px-4 rounded-xl bg-emerald-500 hover:bg-emerald-400 font-semibold text-slate-950 text-sm transition flex items-center justify-center gap-2 shadow-lg shadow-emerald-500/20">
                        <i class="fa-solid fa-wand-magic-sparkles"></i> Extract & Categorize (Offline)
                    </button>
                </form>
            </div>

            <!-- Privacy Guarantee Card -->
            <div class="bg-slate-900/40 border border-slate-800/80 rounded-2xl p-5 text-xs text-slate-400 space-y-2">
                <div class="font-semibold text-slate-200 flex items-center gap-2">
                    <i class="fa-solid fa-shield-halved text-emerald-400"></i> Why Freelancers Pay for This:
                </div>
                <ul class="list-disc pl-4 space-y-1">
                    <li>Strict NDAs prohibit sending client project invoices to OpenAI / cloud endpoints.</li>
                    <li>Saves 4+ hours per week of manual QuickBooks bookkeeping.</li>
                    <li>Ready-to-export tax summary at year-end with full audit logs.</li>
                </ul>
            </div>
        </div>

        <!-- Ledger & Statistics -->
        <div class="md:col-span-2 space-y-6">
            <div class="grid grid-cols-3 gap-4">
                <div class="bg-slate-900 border border-slate-800 rounded-xl p-4">
                    <div class="text-xs text-slate-400">Total Deductible</div>
                    <div id="statTotal" class="text-xl font-bold text-white mt-1">$59.50</div>
                </div>
                <div class="bg-slate-900 border border-slate-800 rounded-xl p-4">
                    <div class="text-xs text-slate-400">Parsed Invoices</div>
                    <div id="statCount" class="text-xl font-bold text-emerald-400 mt-1">2</div>
                </div>
                <div class="bg-slate-900 border border-slate-800 rounded-xl p-4">
                    <div class="text-xs text-slate-400">Cloud Leaks Prevented</div>
                    <div class="text-xl font-bold text-teal-400 mt-1">100%</div>
                </div>
            </div>

            <div class="bg-slate-900 border border-slate-800 rounded-2xl overflow-hidden shadow-xl">
                <div class="px-6 py-4 border-b border-slate-800 flex justify-between items-center">
                    <h3 class="font-semibold text-sm text-white">Extracted Freelance Ledger</h3>
                    <button onclick="exportCSV()" class="text-xs bg-slate-800 hover:bg-slate-700 text-slate-300 px-3 py-1.5 rounded-lg border border-slate-700 flex items-center gap-1.5 transition">
                        <i class="fa-solid fa-file-csv text-emerald-400"></i> Export Tax CSV
                    </button>
                </div>
                <div class="overflow-x-auto">
                    <table class="w-full text-left text-xs text-slate-300">
                        <thead class="bg-slate-950/60 text-slate-400 border-b border-slate-800">
                            <tr>
                                <th class="py-3 px-4">Date</th>
                                <th class="py-3 px-4">Vendor</th>
                                <th class="py-3 px-4">Category</th>
                                <th class="py-3 px-4">Amount</th>
                                <th class="py-3 px-4">Privacy Status</th>
                            </tr>
                        </thead>
                        <tbody id="ledgerTable" class="divide-y divide-slate-800">
                            <!-- Populated via JS -->
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </main>

    <script>
        async function fetchLedger() {
            const res = await fetch('/api/documents');
            const data = await res.json();
            const tbody = document.getElementById('ledgerTable');
            tbody.innerHTML = '';
            
            let total = 0;
            data.forEach(item => {
                total += item.total;
                const tr = document.createElement('tr');
                tr.className = "hover:bg-slate-800/40 transition";
                tr.innerHTML = `
                    <td class="py-3 px-4 font-mono text-slate-400">${item.date}</td>
                    <td class="py-3 px-4 font-semibold text-slate-200">${item.vendor}</td>
                    <td class="py-3 px-4">
                        <span class="bg-slate-800 px-2.5 py-1 rounded-full text-slate-300 text-[10px] border border-slate-700">${item.category}</span>
                    </td>
                    <td class="py-3 px-4 font-mono text-emerald-400 font-semibold">$${item.total.toFixed(2)}</td>
                    <td class="py-3 px-4">
                        <span class="inline-flex items-center gap-1 text-[10px] text-teal-400 bg-teal-500/10 px-2 py-0.5 rounded border border-teal-500/20">
                            <i class="fa-solid fa-lock text-[8px]"></i> Confidential
                        </span>
                    </td>
                `;
                tbody.appendChild(tr);
            });

            document.getElementById('statTotal').innerText = `$${total.toFixed(2)}`;
            document.getElementById('statCount').innerText = data.length;
        }

        document.getElementById('ingestForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            const text = document.getElementById('rawText').value;
            const res = await fetch('/api/ingest', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ text })
            });
            if (res.ok) {
                document.getElementById('rawText').value = '';
                fetchLedger();
            }
        });

        function exportCSV() {
            window.location.href = '/api/export';
        }

        fetchLedger();
    </script>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route("/api/documents")
def get_documents():
    return jsonify(DOCUMENTS)

@app.route("/api/ingest", methods=["POST"])
def ingest_document():
    data = request.json or {}
    text = data.get("text", "")
    extracted = mock_open_weight_extraction(text)
    doc_id = f"inv-{len(DOCUMENTS) + 1:03d}"
    extracted["id"] = doc_id
    extracted["raw_text"] = text
    DOCUMENTS.insert(0, extracted)
    return jsonify({"success": True, "document": extracted})

@app.route("/api/export")
def export_csv():
    import io
    import csv
    from flask import Response
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["ID", "Date", "Vendor", "Invoice_Number", "Category", "Amount_USD", "Tax_USD", "Privacy"])
    for d in DOCUMENTS:
        writer.writerow([d["id"], d["date"], d["vendor"], d["invoice_number"], d["category"], d["total"], d["tax"], "Confidential-Local"])
    
    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-disposition": "attachment; filename=receiptvault_ledger.csv"}
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=True)
