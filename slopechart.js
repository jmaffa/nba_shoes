const bpmData = [
  { star: "Kobe Bryant", season1: 0.0, season2: 0.0 },
  { star: "Kevin Durant", season1: 4.0, season2: 3.2 },
  { star: "LeBron James", season1: 6.5, season2: 5.6 },
  { star: "Sabrina Ionescu", season1: 0.0, season2: -0.4 },
  { star: "Giannis Antetokounmpo", season1: 9.0, season2: 9.5 },
  { star: "Kyrie Irving", season1: 4.9, season2: 3.4 },
  { star: "Ja Morant", season1: 3.1, season2: 2.4 },
  { star: "Damian Lillard", season1: 2.1, season2: 4.0 },
  { star: "James Harden", season1: 4.1, season2: 4.3 },
  { star: "Paul George", season1: 3.2, season2: -0.4 },
  { star: "Devin Booker", season1: 3.0, season2: 0.4 },
  { star: "Donovan Mitchell", season1: 5.8, season2: 3.7 },
  { star: "Michael Jordan", season1: 0.0, season2: 0.0 },
  { star: "Luka Doncic", season1: 9.9, season2: 6.7 },
  { star: "Anthony Edwards", season1: 3.3, season2: 4.3 },
  { star: "Jayson Tatum", season1: 5.1, season2: 5.2 },
  { star: "LaMelo Ball", season1: 3.3, season2: 3.2 },
  { star: "Stephen Curry", season1: 5.2, season2: 6.3 },
  { star: "Zion Williamson", season1: 3.8, season2: 7.0 },
];

const usageData = [
  { star: "Kobe Bryant", season1: 328, season2: 354 },
  { star: "Kevin Durant", season1: 208, season2: 127 },
  { star: "LeBron James", season1: 170, season2: 74 },
  { star: "Sabrina Ionescu", season1: 106, season2: 140 },
  { star: "Giannis Antetokounmpo", season1: 105, season2: 44 },
  { star: "Kyrie Irving", season1: 97, season2: 63 },
  { star: "Ja Morant", season1: 75, season2: 73 },
  { star: "Damian Lillard", season1: 74, season2: 77 },
  { star: "James Harden", season1: 69, season2: 58 },
  { star: "Paul George", season1: 52, season2: 22 },
  { star: "Devin Booker", season1: 49, season2: 118 },
  { star: "Donovan Mitchell", season1: 43, season2: 50 },
  { star: "Michael Jordan", season1: 40, season2: 43 },
  { star: "Luka Doncic", season1: 35, season2: 22 },
  { star: "Anthony Edwards", season1: 23, season2: 50 },
  { star: "Jayson Tatum", season1: 21, season2: 22 },
  { star: "LaMelo Ball", season1: 17, season2: 16 },
  { star: "Stephen Curry", season1: 14, season2: 17 },
  { star: "Zion Williamson", season1: 12, season2: 8 },
];

const notesData = [
  {
    star: "Kobe Bryant",
    note: "Kobe Bryant was retired in both seasons and has no BPM data. He was previously signed with Adidas.",
    image: "kobe.png",
    alt: "Kobe 4",
    cap: "Nike Kobe line",
  },
  {
    star: "Sabrina Ionescu",
    note: "Sabrina Ionescu played in the 2023 and 2024 WNBA seasons. While there is no readily available Box +/- data for these seasons, her <a href='https://www.nbastuffer.com/analytics101/player-impact-estimate-pie/' target='_blank'>Player Impact Estimate</a> went from 13.8 to 13.4 hence the difference captured on the chart. ",
    image: "sabrina.png",
    alt: "Sabrina 1",
    cap: "Nike Sabrina line",
  },
  {
    star: "Michael Jordan",
    note: "Michael Jordan was retired in both seasons and has no BPM data.",
    image: "jordan.png",
    alt: "Jordan 1",
    cap: "Nike Air Jordan brand",
  },
  { star: "Kevin Durant", image: "kd.png", alt: "KD 4", cap: "Nike KD line" },
  { star: "LeBron James", image: "lebron.png", alt: "LeBron 15", cap: "Nike LeBron line" },
  {
    star: "Giannis Antetokounmpo",
    image: "giannis.png",
    alt: "Freak 5",
    cap: "Nike Freak line",
  },
  { star: "Kyrie Irving", note: "Kyrie Irving was previously signed with Nike.", image: "kyrie.png", alt: "Kai 2", cap: "Anta Kai line" },
  { star: "Ja Morant", image: "ja.png", alt: "Ja 1", cap: "Nike Ja line" },
  { star: "Damian Lillard", image: "dame.png", alt: "Dame 9", cap: "adidas Dame line" },
  { star: "James Harden", image: "harden.png", alt: "Harden Vol. 9", cap: "adidas Harden line" },
  { star: "Paul George", image: "pg.png", alt: "PG 2", cap: "Nike PG line" },
  { star: "Devin Booker", image: "book.png", alt: "Book 1", cap: "Nike Book line" },
  { star: "Donovan Mitchell", image: "spida.png", alt: "D.O.N. Issue 3", cap: "adidas D.O.N. line" },
  { star: "Luka Doncic", image: "luka.png", alt: "Luka 1", cap: "Nike Jordan Luka line" },
  { star: "Anthony Edwards", image: "ant.png", alt: "AE 1", cap: "adidas AE line" },
  { star: "Jayson Tatum", image: "tatum.png", alt: "Tatum 1", cap: "Nike Jordan Tatum line" },
  { star: "LaMelo Ball", image: "melo.png", alt: "MB.02", cap: "Puma MB line" },
  { star: "Stephen Curry", image: "curry.png", alt: "Curry 11", cap: "Under Armour Curry brand" },
  { star: "Zion Williamson", image: "kd.png", alt: "Zion 1", cap: "Nike Jordan Zion line" },
];

function updateTooltipAndHighlight(star) {
  const cls = cssSafe(star);

  d3.selectAll(".highlight").classed("highlight", false);
  d3.selectAll(`.line-${cls}`).classed("highlight", true);
  d3.selectAll(`.circle-${cls}`).classed("highlight", true);

  const bpm = bpmData.find((e) => e.star === star);
  const usage = usageData.find((e) => e.star === star);

  d3.select("#tooltip-name").text(star);
  d3.select("#bpm23").text(bpm?.season1 ?? "N/A");
  d3.select("#bpm24").text(bpm?.season2 ?? "N/A");
  d3.select("#usage23").text(usage?.season1 ?? "N/A");
  d3.select("#usage24").text(usage?.season2 ?? "N/A");

  const imgFile = cssSafe(star) + ".jpg";
  d3.select("#tooltip-img")
    .attr("src", `shoes/${imgFile}`)
    .attr("alt", `${star}'s signature shoe`);

  tooltip.style("visibility", "visible");
}


const tooltip = d3.select("#tooltip");

function drawSlopeChart(svgId, data, yLabel, yAxisSide = "left") {
  const width = 500;
  const height = 400;

  const svg = d3.select(svgId).attr("width", width).attr("height", height);

  const margin = { top: 20, right: 60, bottom: 20, left: 60 };

  const x = d3
    .scalePoint()
    .domain(["2023-24", "2024-25"])
    .range([margin.left, width - margin.right]);

  const y = d3
    .scaleLinear()
    .domain([
      d3.min(data, (d) => Math.min(d.season1, d.season2)) - 1,
      d3.max(data, (d) => Math.max(d.season1, d.season2)) + 1,
    ])
    .range([height - margin.bottom, margin.top]);

  const color = d3
    .scaleOrdinal(d3.schemeTableau10)
    .domain(data.map((d) => d.star));

  svg
    .append("g")
    .attr("transform", `translate(0,${height - margin.bottom})`)
    .call(d3.axisBottom(x))
    .call(d3.axisBottom(x).tickSize(0))
    .call((g) => g.select(".domain").remove()); // 🔥 removes x-axis line

  const isRight = yAxisSide === "right";
  const yAxisGenerator = isRight
    ? d3.axisRight(y).tickSize(0).tickPadding(10)
    : d3.axisLeft(y).tickSize(0).tickPadding(10);
  const yAxisX = isRight ? width - margin.right : margin.left;

  svg
    .append("g")
    .attr("transform", `translate(${yAxisX},0)`)
    .call(yAxisGenerator)
    .call((g) => g.select(".domain").remove());
  // svg
  //   .append("g")
  //   .attr("transform", `translate(${yAxisX},0)`)
  //   .call(d3.axisLeft(y).tickSize(0))
  //   .call(d3.axisLeft(y).tickPadding(20))
  //   .call((g) => g.select(".domain").remove());  // 🔥 removes x-axis line

  const lines = svg
    .append("g")
    .selectAll(".line-group")
    .data(data)
    .enter()
    .append("g")
    .attr("class", "line-group")
    .on("mouseover", function (event, d) {
      const cls = cssSafe(d.star);
      d3.selectAll(".highlight").classed("highlight", false);
      d3.selectAll(`.line-${cls}`).classed("highlight", true);
      d3.selectAll(`.circle-${cls}`).classed("highlight", true);

      // Look up full info from both data sets
      const bpm = bpmData.find((e) => e.star === d.star);
      const usage = usageData.find((e) => e.star === d.star);
      const notes = notesData.find((e) => e.star === d.star);

      d3.select("#tooltip-name").text(d.star);
      if (notes?.note) {
        d3.select("#tooltip-note")
          .html(notes.note) // ← use html() instead of text()
          .style("visibility", "visible")
          .style("font-style", "italic");
      } else {
        d3.select("#tooltip-note").text("").style("visibility", "hidden");
      }


      d3.select("#bpm23").text(bpm?.season1 ?? "N/A");
      d3.select("#bpm24").text(bpm?.season2 ?? "N/A");
      d3.select("#usage23").text(usage?.season1 ?? "N/A");
      d3.select("#usage24").text(usage?.season2 ?? "N/A");

      // const imgFile = cssSafe(d.star) + ".jpg";
      d3.select("#tooltip-img")
        .attr("src", `shoe_images/${notes.image}`)
        .attr("alt", `${d.star}'s signature shoe`);
      d3.select("#caption").text(notes?.cap ?? "N/A");
      // tooltip.style("visibility", "visible");
      // Make all children inside the tooltip visible
      tooltip.selectAll("*").style("visibility", "visible");

    })
    .on("mouseout", function () {
      // d3.selectAll(".highlight").classed("highlight", false);
    });

  lines
    .append("line")
    .attr("class", (d) => `line line-${cssSafe(d.star)}`)
    .attr("x1", x("2023-24"))
    .attr("y1", (d) => y(d.season1))
    .attr("x2", x("2024-25"))
    .attr("y2", (d) => y(d.season2));

  lines
    .append("circle")
    .attr("class", (d) => `circle circle-${cssSafe(d.star)}`)
    .attr("cx", x("2023-24"))
    .attr("cy", (d) => y(d.season1))
    .attr("r", 3);

  lines
    .append("circle")
    .attr("class", (d) => `circle circle-${cssSafe(d.star)}`)
    .attr("cx", x("2024-25"))
    .attr("cy", (d) => y(d.season2))
    .attr("r", 3);

  // lines
  //   .append("text")
  //   .attr("x", x("2024-25") + 5)
  //   .attr("y", (d) => y(d.season2))
  //   .attr("alignment-baseline", "middle")
  //   .attr("class", "label")
  //   .text((d) => d.star);

  // Dotted vertical season lines
  ["2023-24", "2024-25"].forEach((season) => {
    svg.append("line")
    .attr("x1", x(season))
    .attr("x2", x(season))
    .attr("y1", margin.top)
    .attr("y2", height - margin.bottom)
    .attr("stroke", "#999")
    .attr("stroke-width", 2)
    .attr("stroke-dasharray", "0,8")           // long gaps, zero-length dashes
    .attr("stroke-linecap", "round");          // makes each dash a rounded dot
    })

  svg
    .append("text")
    .attr("x", margin.left)
    .attr("y", margin.top - 5)
    .text(yLabel)
    .style("font-weight", "bold");
}

function cssSafe(name) {
  return name.toLowerCase().replace(/[^a-z0-9]/g, "-");
}

drawSlopeChart("#chart1", bpmData, "Box +/- (BPM)", "left");
drawSlopeChart("#chart2", usageData, "# of players who wore their shoes", "right");
