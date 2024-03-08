# playMigrate

Aplicación de Python para administrar y migrar playlists entre diversos servicios de streaming de audio (Spotify, Tidal, Youtube Music ...)

## 💻 Lenguaje y Módulos de Terceros

- [**Python**](https://www.python.org/downloads/) - Lenguaje del script Python 3+.
- [**Spotipy**](https://pypi.org/project/spotipy/) - Interacción con la API de Spotify.
- [**Google-api-python-client**](https://pypi.org/project/google-api-python-client/) - Interacción con la API de Google (Youtube API).
- [**Dotenv**](https://pypi.org/project/python-dotenv/) - Manejo de variables de entornos.

## ⌨️ Comandos disponibles

|     | Comando          | Acción                                        |
| :-- | :--------------- | :-------------------------------------------- |
| ⚙️  | `playMigrate.py youtube -l` | Lista todas las playlists de Youtube Music.  |
| ⚙️  | `playMigrate.py youtube -i`          | Muestra información del usuario de Youtube Music. (Canciones y discos más escuchados, minutos reproducidos en la semana ...)      |
| ⚙️  | `playMigrate.py youtube -u`        | Actualiza las credenciales del usuario de Youtube Music. |
| ⚙️  | `playMigrate.py youtube -c playlist_name `        | Crea una nueva playlist de nombre 'playlist_name' en Youtube Music. |
| ⚙️  | `playMigrate.py youtube -t playlist_name`        | Lista las pistas de la playlist 'playlist_name' de Youtube Music con información de interés. |
| ⚙️  | `playMigrate.py spotify youtube -m playlist_name`        | Migra las pistas de la playlist 'playlist_name' del usuario de Spotify a Youtube Music. |
| ⚙️  | `playMigrate.py spotify -l` | Lista todas las playlists de Spotify.  |
| ⚙️  | `playMigrate.py spotify -csv playlist_name` | Descarga información y contenido de la playlist en formáto CSV.  |
| ⚙️  | `playMigrate.py spotify -json playlist_name` | Descarga información y contenido de la playlist en formáto JSON.  |
| ⚙️  | `playMigrate.py spotify -xlsx playlist_name` | Descarga información y contenido de la playlist en formáto XLSX.  |
| ⚙️  | `playMigrate.py spotify -i`          | Muestra información del usuario de Spotify. (Canciones y discos más escuchados, minutos reproducidos en la semana ...)      |
| ⚙️  | `playMigrate.py spotify -u`        | Actualiza las credenciales del usuario de Spotify. |
| ⚙️  | `playMigrate.py spotify -c playlist_name`        | Crea una nueva playlist de nombre 'playlist_name' en Spotify. |
| ⚙️  | `playMigrate.py spotify -t playlist_name`        | Lista las pistas de la playlist 'playlist_name' de Spotify con información de interés. |
| ⚙️  | `playMigrate.py youtube spotify -m playlist_name`        | Migra las pistas de la playlist 'playlist_name' del usuario de Youtube Music a Spotify. |


## 💾 Licencia

[MIT](LICENSE.txt) - Aplicación creada por [**hectorgarciatw**](https://hectorgarcia.vercel.app/).
