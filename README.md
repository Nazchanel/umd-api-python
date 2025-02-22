# UMD API

## UMD API Docs (`umd_api/general`)
[https://beta.umd.io/](https://beta.umd.io/)

## PlanetTerp (`umd_api/planet_terp`)
[https://planetterp.com/api/](https://planetterp.com/api/)

## Weather (`umd_api/weather`)
[https://weather.umd.edu](https://weather.umd.edu)

## PyPI
[https://pypi.org/project/umd-api](https://pypi.org/project/umd-api)


## Installation
```bash
pip install umd-api
```

## Initialization

```python
from umd_api.general import Bus, Courses, Majors, Map, Professors 

bus = Bus()
courses = Courses()
majors = Majors()
map_ = Map()
professors = Professors()
```

```python
from umd_api.planet_terp import Search, Grades, Professors, Courses

search = Search()
grades = Grades()
professors = Professors()
courses = Courses()
```

```python
from umd_api.weather import Weather, Forecast

weather = Weather()
forecast = Forecast()
```

## Modules

<details>
<summary><strong>General</strong></summary>

**Bus**
- `list_routes()`
- `view_specific_routes(route_ids)`
- `list_stops()`
- `get_specific_stops(stop_ids : list)`
- `current_bus_locations_by_route(route_id)` **(UMD.IO API IS BROKEN HERE)**
- `bus_schedules(route_id)`
- `get_arrivals_for_stop(route_id, stop_id)`

---

**Courses**
- `list_courses(sort=None, page=None, per_page=None, semester=None, credits=None, dept_id=None, gen_ed=None)`
- `list_minified_courses(sort=None, page=None, per_page=None, semester=None)`
- `list_sections(sort=None, page=None, per_page=None, course_id=None, seats=None, open_seats=None, waitlist=None, semester=None)`
- `view_specific_sections(section_ids : list)`
- `view_specific_courses(course_ids : list, semester=None)`
- `view_sections_for_course(course_ids : list, semester=None)`
- `view_specific_sections_for_course(course_ids : list, section_ids : list)`
- `list_semesters()`
- `list_departments()`

---

**Majors**
- `list_majors()`

---

**Map**
- `list_buildings()`
- `get_buildings(building_id : list)`

---

**Professors**
- `get_professor(name: str, reviews=False)`
- `get_all_professors(type=None, reviews=False, limit=100, offset=0)`
</details>

<details>
<summary><strong>PlanetTerp</strong></summary>

**Search**
- `search(query, limit=30, offset=0)`

---

**Grades**
- `get_grades(course=None, professor=None, semester=None, section=None)`

---

**Professors**
- `get_professor(name: str, reviews=False)`
- `get_all_professors(type=None, reviews=False, limit=100, offset=0)`

---

**Courses**
- `get_course(name, reviews=False)`
- `get_courses(department=None, reviews=False, limit=100, offset=0)`
</details>
<details>
<summary><strong>Weather</strong></summary>

**Weather**
- `get_weather_data(station="", start_time="", end_time=")`
- `get_hourly_forecast()`
- `save_radar_gif()`
- `get_weather_descrption()`
---

**Forecast**
- `get_hourly_forecast()`
- `get_weekly_forecast()`

</details>


### Wakatime (Time Spent Programming)

[![wakatime](https://wakatime.com/badge/user/d2cf396a-1b98-4795-9559-b880684c63b7/project/6064c94d-4e62-413f-8e6f-68c974df4e07.svg)](https://wakatime.com/badge/user/d2cf396a-1b98-4795-9559-b880684c63b7/project/6064c94d-4e62-413f-8e6f-68c974df4e07)

[![wakatime](https://wakatime.com/badge/user/d2cf396a-1b98-4795-9559-b880684c63b7/project/8dd367da-8a21-4a43-9308-b02267536c0f.svg)](https://wakatime.com/badge/user/d2cf396a-1b98-4795-9559-b880684c63b7/project/8dd367da-8a21-4a43-9308-b02267536c0f)

Combine the two for total time
