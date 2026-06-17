# Changelog — финальный проект «Прагматик» (corp_django_course3)

> Финальный проект курса «Настройка проекта на Django». Бизнес-логика написана
> с нуля по готовым моделям и вёрстке (legacy/baseline нет). Документирует команды
> и изменения по файлам. Все пути — **относительно текущей папки**.
>
> Две рабочие директории:
> - **корень репо** `corp_django_course3/` — `pytest.ini`, `.flake8`; отсюда
>   `git`, `pytest`, `flake8`;
> - **`pragmatic/`** — `manage.py`; отсюда команды `manage.py`.
>
> Восстановлено по финальному состоянию проекта.

---

## 1. Получение репозитория

В рабочей папке `dev/` (форк создан под KuzmichVK):

```bash
git clone git@github.com:KuzmichVK/corp_django_course3.git
```

```bash
cd corp_django_course3
```

```bash
code .
```

> Дальше все команды — из этой папки (корень репо), если не сказано иное.
> Шаблоны уже лежат в `pragmatic/templates/` (предоставлены) — отдельного
> переноса вёрстки не требуется.

---

## 2. Окружение

Из корня репо. Python 3.10 (под Django 3.2):

```bash
uv venv --python 3.10
```

```bash
uv pip install -r requirements.txt
```

---

## 3. Новое приложение `users`

Из `pragmatic/` (модель пользователя — встроенная, НЕ переопределяется):

```bash
cd pragmatic
```

```bash
uv run python manage.py startapp users
```

```bash
cd ..
```

Затем `users` добавлено в `INSTALLED_APPS` (см. раздел 5).

---

## 4. Изменения по файлам (реализация, всё на CBV)

### `pragmatic/courses/models.py`

- добавлен `get_absolute_url`: **Category** → `courses:category_detail` (по slug),
  **Course** → `courses:course_detail` (по pk). Поля моделей даны заготовкой;
  флаг публичности курса — `is_public`.

### `pragmatic/lessons/models.py`

- добавлен `get_absolute_url`: **Lesson** → `lessons:lesson_detail` (по pk).

### `pragmatic/courses/urls.py` (новый), `app_name = 'courses'`

- `category/` → `category_list`;
- `category/<slug:slug>/` → `category_detail`;
- `` (пусто) → `index`;
- `<int:pk>/` → `course_detail`;
- `<int:pk>/lesson/` → `create_lesson`;
- `<int:pk>/lesson/<int:lesson_id>/edit/` → `edit_lesson`;
- `<int:pk>/lesson/<int:lesson_id>/delete/` → `delete_lesson`.

> Нюанс: три последних маршрута ведут на классы `Lesson*View` из приложения
> **lessons**, но зарегистрированы здесь под namespace **courses** (`courses:`).
> Импорт: `from lessons import views as lessons_views`.

### `pragmatic/courses/views.py` (новый)

- хелпер `visible_courses(qs, user)`: аноним → `filter(is_public=True)`,
  авторизованный → все;
- `CategoryListView` (список категорий, **без** пагинации);
- `CategoryDetailView` (`SingleObjectMixin` + `ListView`, курсы категории,
  пагинация 3, фильтр публичности);
- `CourseListView` (список курсов, пагинация 3, фильтр публичности);
- `CourseDetailView` (курс + уроки в контексте, фильтр публичности → непубличный
  для анонима даёт 404).

### `pragmatic/lessons/urls.py` (новый), `app_name = 'lessons'`

- `<int:pk>/` → `lesson_detail`.

### `pragmatic/lessons/views.py` (новый)

- `LessonDetailView` (для анонима — только уроки публичных курсов);
- `AuthorCourseRequiredMixin(LoginRequiredMixin)`: в `dispatch` для авторизованного
  — `get_object_or_404(Course, pk, author=request.user)` (не-автор → 404), для
  анонима — `LoginRequiredMixin` (редирект на логин);
- `LessonCreateView` (`fields=('title','text','type','duration')`, шаблон
  `lessons/lesson_form.html`, курс проставляется в `form_valid`);
- `LessonUpdateView` (тот же шаблон, kwarg `lesson_id`);
- `LessonDeleteView` (шаблон `lessons/lesson_confirm_delete.html`, после удаления →
  `courses:course_detail`).

> Редиректы: create/edit → страница урока (`get_absolute_url` урока), delete →
> страница курса.

### `pragmatic/users/urls.py` (новый), `app_name = 'users'`

- `<str:username>/profile/` → `profile`.

### `pragmatic/users/views.py` (новый)

- `UserRegistrationCreateView` (`CreateView` + `UserCreationForm`, шаблон
  `registration/registration_form.html`, `success_url = reverse_lazy('login')`);
- `UserProfileDetailView` (`DetailView` по `User`, ключ контекста `profile`,
  поиск по `username`): в контекст `courses` (для анонима — только публичные,
  сортировка `-created_at`) и `courses_count`
  (`values('is_public').annotate(count=Count('id'))`).

### `pragmatic/pragmatic/urls.py`

- маршрут регистрации `auth/registration/`, `name='registration'` (без namespace);
- `path('auth/', include('django.contrib.auth.urls'))`;
- подключены `users.urls`, `courses.urls`, `lessons.urls`;
- корень `/` редиректит на `courses:index`.

### `pragmatic/pragmatic/settings.py`

- `users` в `INSTALLED_APPS`;
- `LOGIN_URL = 'login'`, `LOGIN_REDIRECT_URL = 'courses:index'`;
- почта — файловый бэкенд:
  `EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'`,
  `EMAIL_FILE_PATH = BASE_DIR / 'sent_emails'`.

### `.gitignore`

- проверено/добавлено `sent_emails/` (каталог «отправленных» писем не отслеживается).

---

## 5. Миграции

Создать БД (модели `courses`/`lessons` готовы; у `users` своих моделей нет).
Из `pragmatic/`:

```bash
cd pragmatic
```

```bash
uv run python manage.py makemigrations
```

```bash
uv run python manage.py migrate
```

```bash
cd ..
```

> Результат: `courses/migrations/0001_initial.py`, `lessons/migrations/0001_initial.py`.
> У `users` миграций нет (нет своих моделей) — это нормально.

---

## 6. Почта (файловый бэкенд)

Реальный SMTP не нужен — письма копятся в файлы (`settings.py`, раздел 4),
`sent_emails/` исключён из git.

> Нюанс: тест `test_emails` импортирует `locmem`-бэкенд, но Django в тестовом
> окружении сам подменяет `settings.EMAIL_BACKEND` на `locmem` — поэтому проверка
> проходит и при `filebased` в `settings.py`, а `EMAIL_FILE_PATH` тест читает
> напрямую (должен быть `BASE_DIR/'sent_emails'`). Оставлен `filebased`, как
> требует задание.

---

## 7. Проверки перед коммитом

Из корня репо (там `pytest.ini` и `.flake8`):

```bash
uv run flake8 .
```

```bash
uv run pytest
```

> ⚠️ `pytest`/`flake8` — **только из корня репо**. Из вложенной `pragmatic/`
> pytest соберёт 0 тестов.
>
> ⚠️ `flake8` показывает несколько E501 в `courses/models.py` и `lessons/models.py`
> (длинные `help_text`/`verbose_name`) — это заготовленные Практикумом модели,
> не написанный код. На грейдер (pytest) не влияет. При желании — переоформить
> переносом строк (значения не меняются → миграции не трогаются).

---

## 8. Git

Из корня репо. Перед коммитом — проверить индекс:

```bash
git status
```

```bash
git ls-files | grep -E 'db.sqlite3|/media/|sent_emails|.venv|__pycache__'
```

> Вывод последней команды должен быть **пустым**.

Коммиты (осмысленные, по блокам):

```bash
git add .
```

```bash
git commit -m "feat: users app, registration, profile"
```

```bash
git commit -m "feat: courses views and urls with publicity filter"
```

```bash
git commit -m "feat: lessons CRUD by course author (404 for non-author)"
```

```bash
git commit -m "chore: filebased email, get_absolute_url, gitignore sent_emails"
```

Пуш в ветку форка `master`:

```bash
git push
```

---

## Итог проекта

- Закрыты блоки: пользователи (регистрация/аутентификация/профиль), просмотр
  курсов с фильтром публичности (аноним — только публичные, непубличный → 404),
  пагинация по 3, CRUD уроков только автором курса (иначе 404), файловая почта.
- Всё на классовых представлениях; ключевая тонкость — классы `Lesson*View` из
  приложения `lessons` под namespace `courses`.
- Цель — зелёный `uv run pytest` из корня репо.
