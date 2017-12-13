# offsets-api

To generate a database diagram, install graphviz https://graphviz.gitlab.io/_pages/Download/Download_windows.html and run the following commands:

Then run:
python manage.py graph_models core > my_project.dot
"C:\Program Files (x86)\Graphviz2.38\bin\dot.exe" my_project.dot -Tpng -o app.png
