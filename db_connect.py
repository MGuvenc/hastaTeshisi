from database import *

conn = create_connection('hasta_teshis.db')
create_tables(conn)
close_connection(conn)