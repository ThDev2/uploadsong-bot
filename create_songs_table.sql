CREATE TABLE custom_songs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    song_id INT UNIQUE,
    title VARCHAR(255),
    author VARCHAR(255),
    youtube_url TEXT,
    uploader VARCHAR(255),
    gdps_link TEXT,
    upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);