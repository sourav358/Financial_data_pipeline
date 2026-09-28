
document.querySelectorAll(".tab").forEach(btn => {
    btn.addEventListener("click", () => {
        document.querySelectorAll(".tab")
            .forEach(t => t.classList.remove("active"));

        document.querySelectorAll(".tab-panel")
            .forEach(p => p.classList.remove("active"));

        btn.classList.add("active");

        document
            .getElementById("tab-" + btn.dataset.tab)
            .classList.add("active");
    });
});


// FETCH CSV
async function fetchCSV(url) {
    try {
        const r = await fetch(url);
        if (!r.ok) throw new Error(r.status);
        return await r.text();
    } catch (e) {
        console.error(url, e);
        return null;
    }
}


// PARSE CSV
function parseCSV(text) {
    const lines = text.trim().split("\n");

    return {
        headers: lines[0].split(",").map(x => x.trim()),
        rows: lines.slice(1)
            .map(x => x.split(",").map(v => v.trim()))
    };
}


// NUMBER FORMAT
function formatNumber(value) {
    const n = parseFloat(value);

    if (isNaN(n)) return value || "—";

    return n.toLocaleString("en-IN", {
        maximumFractionDigits: 2
    });
}


// TABLE
function buildTable(headers, rows) {

    const table = document.createElement("table");
    table.className = "data-table";

    const thead = table.createTHead();
    const hrow = thead.insertRow();

    headers.forEach((h, i) => {
        const th = document.createElement("th");
        th.textContent =
            i === 0 ? "Particulars" : h;
        hrow.appendChild(th);
    });

    const tbody = table.createTBody();

    rows.forEach(row => {

        const tr = tbody.insertRow();

        row.forEach((cell, i) => {

            const td = tr.insertCell();

            td.textContent =
                i === 0 ? cell : formatNumber(cell);

        });
    });

    return table;
}


// LOAD DATA
async function loadAll() {

    const files = [
        ["pl-container", "../data/processed/profit_loss.csv"],
        ["bs-container", "../data/processed/balance_sheet.csv"],
        ["cf-container", "../data/processed/cash_flow.csv"],
        ["rat-container", "../data/processed/ratios.csv"],
        ["qtr-container", "../data/processed/quarterly_results.csv"]
    ];

    let loaded = 0;
    let datasets = {};

    for (const [container, file] of files) {

        const text = await fetchCSV(file);

        if (!text) continue;

        const data = parseCSV(text);

        datasets[container] = data;

        const el = document.getElementById(container);

        if (el) {
            el.innerHTML = "";
            el.appendChild(
                buildTable(data.headers, data.rows)
            );
        }

        loaded++;
    }


    // PIPELINE STATUS
    document.getElementById("dataset-check").innerHTML =
        loaded === files.length
            ? `✓ ${loaded}/${files.length} datasets loaded`
            : `⚠ ${loaded}/${files.length} datasets loaded`;


    // INTERNAL VALIDATION
    validateProfitLoss(datasets["pl-container"]);
    validateOPM(datasets["pl-container"]);


    // EXTERNAL VALIDATION
    loadExternalValidation();
}


// PROFIT & LOSS CHECK
function validateProfitLoss(data) {

    const box = document.getElementById("profit-check");

    if (!data) {
        box.innerHTML = "⚠ Profit & Loss data unavailable";
        return;
    }

    const sales = findRow(data, ["Sales +", "Sales"]);
    const expenses = findRow(data, ["Expenses +", "Expenses"]);
    const profit = findRow(data, ["Operating Profit"]);

    if (!sales || !expenses || !profit) {
        box.innerHTML = "⚠ Required P&L rows not found";
        return;
    }

    const periods = data.headers.slice(1);
    let errors = [];

    periods.forEach((period, i) => {

        const s = parseFloat(sales[i]);
        const e = parseFloat(expenses[i]);
        const p = parseFloat(profit[i]);

        if (!isNaN(s) && !isNaN(e) && !isNaN(p)) {

            if (Math.abs((s - e) - p) > 0.1) {
                errors.push(period);
            }
        }
    });

    box.innerHTML = errors.length
        ? `⚠ P&L mismatch: ${errors.join(", ")}`
        : "✓ Sales − Expenses = Operating Profit";
}


// OPM CHECK
function validateOPM(data) {
    const box = document.getElementById("opm-check");

    if (!data) {
        box.innerHTML = "⚠ P&L data unavailable";
        return;
    }

    const sales = findRow(data, ["Sales +", "Sales"]);
    const profit = findRow(data, ["Operating Profit"]);
    const opm = findRow(data, ["OPM %", "OPM"]);

    if (!sales || !profit || !opm) {
        box.innerHTML = "⚠ OPM rows not found";
        return;
    }

    const periods = data.headers.slice(1);
    const errors = [];

    periods.forEach((period, i) => {
        const s = parseFloat(sales[i]);
        const p = parseFloat(profit[i]);
        const reported = parseFloat(opm[i]);

        if (!isNaN(s) && !isNaN(p) && !isNaN(reported)) {
            const calculated = (p / s) * 100;
            const difference = calculated - reported;

            if (Math.abs(difference) >= 1) {
                errors.push(
                    `${period}: calculated ${calculated.toFixed(2)}%, ` +
                    `reported ${reported.toFixed(2)}%, ` +
                    `difference ${difference.toFixed(2)}%`
                );
            }
        }
    });

    if (!errors.length) {
        box.innerHTML = "✓ OPM calculation consistent";
    } else {
        box.innerHTML =
            "⚠ OPM mismatches:<br>" +
            errors.map(e => `• ${e}`).join("<br>");
    }
}


// FIND ROW
function findRow(data, names) {

    if (!data) return null;

    const index = data.headers.findIndex(
        h => h.toLowerCase() === "particulars"
    );

    if (index === -1) return null;

    return data.rows.find(row =>
        names.includes(row[index])
    );
}


// EXTERNAL VALIDATION
async function loadExternalValidation() {

    const box = document.getElementById("external-check");

    const text = await fetchCSV(
        "../data/validation_report.csv"
    );

    if (!text) {
        box.innerHTML = "⚠ Validation report not found";
        return;
    }

    const data = parseCSV(text);

    if (!data.rows.length) {
        box.innerHTML = "⚠ Validation report is empty";
        return;
    }

    box.innerHTML = data.rows.map(row => {

        const metric = row[0];
        const difference = row[3];
        const status = row[4];

        return `
            <div class="validation-row">
                ${status === "PASS" ? "✓" : "⚠"}
                <strong>${metric}</strong>
                <span>
                    Difference: ${formatNumber(difference)}
                </span>
                <span>${status}</span>
            </div>
        `;

    }).join("");
}


// START
document.addEventListener("DOMContentLoaded", loadAll);