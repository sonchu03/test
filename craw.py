import csv
import requests

api_key = "8adf491663cadc43f398acb35ef3aac5"
num_movies = 8000  # Số lượng phim bạn muốn lấy dữ liệu

movies_data = []
count = 0

# Lấy dữ liệu của 3000 bộ phim
for page in range(1, (num_movies // 20) + 2):
    url = f"https://api.themoviedb.org/3/movie/popular?api_key={api_key}&language=en-US&page={page}"
    response = requests.get(url)
    data = response.json()

    for movie in data['results']:
        movie_id = movie['id']
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&append_to_response=keywords,credits"
        response = requests.get(url)
        movie_data = response.json()

        # Trích xuất thông tin cần thiết
        movie_info = {
            'id': movie_data['id'],
            'original_title': movie_data['original_title'],
            'keywords': ', '.join([f"'{keyword['name']}'" for keyword in movie_data['keywords']['keywords']]),
            'director': '',
            'cast': ', '.join([f"'{cast_member['name']}'" for cast_member in movie_data['credits']['cast']]),
            'genres': ', '.join([f"'{genre['name']}'" for genre in movie_data['genres']]),
            'vote_average': movie_data['vote_average']
        }
        # Lấy dữ liệu đạo diễn
        if 'crew' in movie_data['credits']:
            for crew_member in movie_data['credits']['crew']:
                if crew_member['job'] == 'Director':
                    movie_info['director'] = crew_member['name']
                    break

        movies_data.append(movie_info)
        count += 1
        print(f"Lấy dữ liệu cho phim thứ {count}/{num_movies}")

        if count == num_movies:
            break

    if count == num_movies:
        break

# Ghi dữ liệu vào file CSV
csv_file = 'TheMovieDB8000.csv'

with open(csv_file, mode='w', newline='', encoding='utf-8-sig') as file:
    writer = csv.writer(file)
    writer.writerow(['ID', 'Title', 'Keywords', 'Director', 'Cast', 'Genres', 'Vote Average'])
    for movie in movies_data:
        writer.writerow([movie['id'], movie['original_title'], movie['keywords'], movie['director'],
                         movie['cast'], movie['genres'], movie['vote_average']])

print("Dữ liệu đã được ghi vào file CSV thành công.")