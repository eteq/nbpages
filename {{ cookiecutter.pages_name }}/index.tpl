<!doctype html>
<html lang=en>
<head>
<meta charset=utf-8>
<title>{{ cookiecutter.pages_name }} Index</title>
</head>
<body>
<ul>
{% raw %}{% for notebook_html_path in notebook_html_paths %}
  <li><a href="{{ notebook_html_path }}">{{ notebook_html_path }}</a></li>
{% endfor %}{% endraw %}
</ul>
</body>
</html>
