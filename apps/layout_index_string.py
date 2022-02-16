nav_div="""
<div class='area'></div>
<nav class="main-menu">
		<ul>
			<li>
				<a href="/index">
					<i class="fa fa-home fa-2x"></i>
					<span class="nav-text">
						Home
					</span>
				</a>
			</li>
			<li class="has-subnav">
				<a href="/dash/dashboard">
					<i class="fa fa-bars fa-2x"></i>
					<span class="nav-text">
						Dashboard
					</span>
				</a>
			</li>
			<li clas
			<li class="has-subnav">
				<a href="#">
					<i class="fa fa-laptop fa-2x"></i>
					<span class="nav-text">
						UI Components
					</span>
				</a>
				
			</li>
			<li class="has-subnav">
				<a href="/dash/list">
					<i class="fa fa-list fa-2x"></i>
					<span class="nav-text">
						Lists
					</span>
				</a>
				
			</li>
			<li class="has-subnav">
				<a href="/dash/store">
					<i class="fa fa-folder-open fa-2x"></i>
					<span class="nav-text">
						Pages
					</span>
				</a>
				
			</li>
			<li>
				<a href="#">
					<i class="fa fa-bar-chart-o fa-2x"></i>
					<span class="nav-text">
						Graphs and Statistics
					</span>
				</a>
			</li>
			<li>
				<a href="#">
					<i class="fa fa-font fa-2x"></i>
					<span class="nav-text">
						Typography and Icons
					</span>
				</a>
			</li>
			<li>
				<a href="#">
					<i class="fa fa-table fa-2x"></i>
					<span class="nav-text">
						Tables
					</span>
				</a>
			</li>
			<li>
				<a href="#">
					<i class="fa fa-map-marker fa-2x"></i>
					<span class="nav-text">
						Maps
					</span>
				</a>
			</li>
			<li>
				<a href="#">
					<i class="fa fa-info fa-2x"></i>
					<span class="nav-text">
						Documentation
					</span>
				</a>
			</li>
		</ul>

		<ul class="logout">
			<li>
				<a href="#">
						<i class="fa fa-power-off fa-2x"></i>
					<span class="nav-text">
						Logout
					</span>
				</a>
			</li>  
		</ul>
	</nav>
"""

index_string = """
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
    </head>
    <body>
"""+nav_div+"""
			<div class="dash_content">
				<div>My Custom header</div>
				{%app_entry%}
				<footer>
					{%config%}
					{%scripts%}
					{%renderer%}
				</footer>
				<div>My Custom footer</div>
			</div>
		</div>
    </body>
</html>
"""