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

<!-- <script src="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.27.4/codemirror.min.js"></script> -->