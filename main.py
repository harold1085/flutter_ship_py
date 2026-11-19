from modulos.supabase_manager import SupabaseManager

supabase = SupabaseManager()

resultado = supabase.probar_conexion()

if resultado:
    print("\nSupabase Storage esta funcionando")
else:
    print("\nNo se pudo conetar ")  