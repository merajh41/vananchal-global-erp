from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter()

@router.get("/docs", include_in_schema=False)
async def custom_swagger():
    return HTMLResponse("""
<!DOCTYPE html>
<html>
<head>
<link rel="stylesheet"
href="https://unpkg.com/swagger-ui-dist/swagger-ui.css">
</head>

<body>

<div id="swagger-ui"></div>

<script src="https://unpkg.com/swagger-ui-dist/swagger-ui-bundle.js"></script>

<script>

window.onload = () => {

const ui = SwaggerUIBundle({
url: "/openapi.json",
dom_id: "#swagger-ui",
persistAuthorization: true
});

document.addEventListener("keydown", function(e){

if(e.key==="Enter"){

const btn=document.querySelector(".auth-btn");

if(btn){
btn.click();
}

}

});

};

</script>

</body>
</html>
""")