//возраст
const birthDate = new Date('2004-05-10T00:00:00'); 

  function updateAge() {
    const now = new Date();
    const diff = now - birthDate; 
    const years = diff / (1000 * 60 * 60 * 24 * 365.2425); 
    document.getElementById('age').textContent = years.toFixed(6); 
  }


  setInterval(updateAge, 10);
//музика)

   async function getTrack() {
            try {
                const response = await fetch("http://127.0.0.1:5000/current_track");
                const data = await response.json();

                if (data.error) {
                    document.getElementById("track-info").innerText = data.error;
                } else {
                    document.getElementById("track-info").innerHTML = `
                        <strong>Трек:</strong> ${data.title} <br>
                        <strong>Исполнитель:</strong> ${data.artists} <br>
                        <strong>Альбом:</strong> ${data.album} <br>
                        <img src="${data.cover}" alt="Обложка" width="200"> <br>
                        <strong>Длительность:</strong> ${data.duration}
                    `;
                }
            } catch (err) {
                document.getElementById("track-info").innerText = "Ошибка подключения к серверу";
            }
        }

        getTrack();
        setInterval(getTrack, 30000);