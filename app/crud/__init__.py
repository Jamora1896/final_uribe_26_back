from app.crud.users import (
    get_user_by_username, get_user_by_id, get_users,
    create_user, update_user, delete_user, authenticate_user,
)
from app.crud.catalog import (
    get_advisors, get_advisor, create_advisor, update_advisor, delete_advisor,
    get_locals, get_local, create_local, update_local, delete_local,
    get_products, get_product, create_product, update_product, delete_product,
)
from app.crud.sales import (
    get_sales, get_sale, create_sale, update_sale, delete_sale,
    get_dashboard_metrics,
)