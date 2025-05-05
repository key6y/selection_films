document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('recommendationForm');
    const resultsDiv = document.getElementById('results');
    const contentTypeSelect = document.querySelector('select[name="content_type"]');
    const seasonsFields = document.getElementById('seasonsFields');
    const showOptionsBtn = document.getElementById('showOptions');
    const optionsDiv = document.getElementById('options');

    // Показывать поля сезонов только для сериалов или "все"
    contentTypeSelect.addEventListener('change', () => {
        const value = contentTypeSelect.value;
        seasonsFields.classList.toggle('hidden', value === 'movie');
    });

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        const formData = new FormData(form);

        try {
            const response = await fetch('/recommend', {
                method: 'POST',
                body: formData
            });
            const data = await response.json();

            if (data.error) {
                resultsDiv.innerHTML = `<p class="text-red-500">Ошибка: ${data.error}</p>`;
                return;
            }

            if (data.recommendations.length === 0) {
                resultsDiv.innerHTML = '<p class="text-gray-500">По вашему запросу ничего не найдено. 😞</p>';
                return;
            }

            let html = '<h2 class="text-xl font-semibold mb-4">Результаты поиска</h2>';
            data.recommendations.forEach((item, index) => {
                html += `
                    <div class="result-item">
                        <p><strong>${index + 1}. ${item.title} (${item.year})</strong></p>
                        <p>Тип: ${item.type}</p>
                        <p>Рейтинг: ${item.rating}</p>
                        <p>Продолжительность: ${item.duration}</p>
                        <p>Жанры: ${item.genres.join(', ')}</p>
                        <p>Режиссёр: ${item.director || 'Не указан'}</p>
                        <p>Страна: ${item.country}, Язык: ${item.language}, Возраст: ${item.age_rating}</p>
                    </div>
                `;
            });
            resultsDiv.innerHTML = html;
        } catch (error) {
            resultsDiv.innerHTML = `<p class="text-red-500">Ошибка: ${error.message}</p>`;
        }
    });

    showOptionsBtn.addEventListener('click', async () => {
        try {
            const response = await fetch('/options');
            const data = await response.json();

            if (data.error) {
                optionsDiv.innerHTML = `<p class="text-red-500">Ошибка: ${data.error}</p>`;
                return;
            }

            optionsDiv.classList.remove('hidden');
            optionsDiv.innerHTML = `
                <h2 class="text-xl font-semibold mb-4">Доступные варианты</h2>
                <p><strong>Жанры:</strong> ${data.genres.join(', ')}</p>
                <p><strong>Актёры:</strong> ${data.actors.join(', ')}</p>
                <p><strong>Режиссёры:</strong> ${data.directors.join(', ')}</p>
            `;
        } catch (error) {
            optionsDiv.innerHTML = `<p class="text-red-500">Ошибка: ${error.message}</p>`;
        }
    });
});