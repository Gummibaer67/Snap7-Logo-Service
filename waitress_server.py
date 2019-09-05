from waitress import serve
import snap7_logo_service

serve(snap7_logo_service.app, host='0.0.0.0', port=5000, threads=8)
