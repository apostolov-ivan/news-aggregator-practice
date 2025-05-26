// Глобальні змінні
let allArticles = [];

const filterSelect = document.getElementById("filter-select");
const tableBody = document.querySelector("#articles-table tbody");
const canvasCtx = document.getElementById("sentiment-chart").getContext("2d");

// 1) Функція завантаження даних
async function loadData() {
  try {
    // 1.1) Підтягуємо новини
    await fetch(`${API_BASE}/fetch/${STUDENT_ID}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" }
    });

    // 1.2) Аналіз тональності
    const res = await fetch(`${API_BASE}/analyze/${STUDENT_ID}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" }
    });
    const data = await res.json();

    // 1.3) Зберігаємо у allArticles
    allArticles = data.articles.map(a => ({
      ...a,
      date: a.published ? new Date(a.published) : new Date()
    }));

    if (allArticles.length === 0) { 
  allArticles = [
    {
      title: "Тестова новина",
      link: "https://example.com",
      published: new Date().toISOString(),
      sentiment: "positive",
      scores: {compound: 0.8},
      date: new Date()
    }
  ];
}

    // Рендеримо вміст
    render();
  } catch (err) {
    console.error("Помилка під час завантаження даних:", err);
  }
}

// 2) Функція рендеру таблиці та діаграми
function render() {
  const filter = filterSelect.value;
  const filtered = allArticles.filter(a =>
    filter === "all" ? true : a.sentiment === filter
  );

  // 2.1) Оновлюємо таблицю
  tableBody.innerHTML = filtered
    .sort((a, b) => b.date - a.date)
    .map(a => `
      <tr>
        <td>${a.date.toLocaleString()}</td>
        <td>${a.sentiment}</td>
        <td><a href="${a.link}" target="_blank">${a.title}</a></td>
      </tr>
    `).join("");

  // 2.2) Підрахунок для діаграми
  const counts = { positive: 0, neutral: 0, negative: 0 };
  filtered.forEach(a => counts[a.sentiment]++);
  chart.data.datasets[0].data = [
    counts.positive,
    counts.neutral,
    counts.negative
  ];
  chart.update();
}

// 3) Ініціалізація Chart.js (кругова діаграма)
const chart = new Chart(canvasCtx, {
  type: 'pie',
  data: {
    labels: ['Позитивні', 'Нейтральні', 'Негативні'],
    datasets: [{
      data: [0, 0, 0],
      backgroundColor: ['#4caf50', '#ffca28', '#f44336']
    }]
  },
  options: {
    responsive: true,
    maintainAspectRatio: true,
    aspectRatio: 2,
    plugins: {
      legend: { position: 'top' }
    }
  }
});

// 4) Обробник зміни фільтра
filterSelect.addEventListener("change", render);

// 5) Завантаження даних при старті
window.addEventListener("load", loadData);
