#!/bin/bash
echo "🔥🔥🔥 MIGRATION COMMENCEE 🔥🔥🔥"
python manage.py migrate --verbosity 3
echo "✅✅✅ MIGRATION TERMINEE ✅✅✅"
gunicorn villana.wsgi:application --bind 0.0.0.0:$PORT