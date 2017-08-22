---
layout: default
title: "Specifications"
---
<div id="page-content">
{% for spec in site.specs %}
  {% if spec.version == site.latest_version %}
    {{ spec.content }}
  {% endif %}
{% endfor %}
</div>