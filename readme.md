

## PyCharm setup
Airflow will run dags by adding in PYTHONPATH environment variable `./plugins` folder from project folder. \
That means - all imports should be relative to `./plugins` module. \
But PyCharm interpreter sees only entire project directory. \
And all imports should be relative to project directory. \
For comfortable development we will add `./plugins` into python interpreter by following steps bellow:

1. Open `File -> Settings -> Python interpreter`
2. Push `Gear icon -> Show all`
3. Push `Tree icon (label: Show paths for selected interpreter)`
4. Push `Plus icon` and add current project path plus `/plugins`

Example: `C:/PyCharmProjects/project_name/plugins`
