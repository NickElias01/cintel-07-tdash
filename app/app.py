# Import necessary libraries
import seaborn as sns  # For creating visualizations
from faicons import icon_svg  # For using Font Awesome icons
from shiny import reactive  # For reactivity (dynamic updates) in PyShiny
from shiny.express import input, render, ui  # For UI elements and rendering outputs
import palmerpenguins  # Dataset for example purposes

# Load the dataset: This is a dataset of penguin measurements
df = palmerpenguins.load_penguins()

# Set up the app's main configuration, such as title and layout properties
ui.page_opts(title="Elias Analytics Penguins Dashboard", fillable=True)

# Define the sidebar for user input and additional links
with ui.sidebar(title="Filter controls"):
    # Slider input to filter penguins by body mass
    ui.input_slider("mass", "Mass", 2000, 6000, 6000)
    
    # Checkbox group for selecting penguin species
    ui.input_checkbox_group(
        "species",
        "Species",
        ["Adelie", "Gentoo", "Chinstrap"],
        selected=["Adelie", "Gentoo", "Chinstrap"],
    )
    
    # Add a horizontal line to visually separate inputs from links
    ui.hr()
    ui.h6("Links")  # Add a section title for external resources
    
    # Links to GitHub and relevant PyShiny documentation/resources
    ui.a(
        "GitHub Source",
        href="https://github.com/denisecase/cintel-07-tdash",
        target="_blank",
    )
    ui.a(
        "GitHub App",
        href="https://nickelias01.github.io/cintel-07-tdash/",
        target="_blank",
    )
    ui.a(
        "GitHub Issues",
        href="https://github.com/NickElias01/cintel-07-tdash",
        target="_blank",
    )
    ui.a("PyShiny", href="https://shiny.posit.co/py/", target="_blank")
    ui.a(
        "Template: Basic Dashboard",
        href="https://shiny.posit.co/py/templates/dashboard/",
        target="_blank",
    )
    ui.a(
        "See also",
        href="https://github.com/denisecase/pyshiny-penguins-dashboard-express",
        target="_blank",
    )

# Main layout: Wrapping the value boxes in a flexible layout container
with ui.layout_column_wrap(fill=False):
    # First value box: Displays the number of filtered penguins
    with ui.value_box(showcase=icon_svg("earlybirds"),style="background-color: lightblue; color: darkblue;"):
        "Number of penguins"

        @render.text
        def count():
            # Calculate and return the number of penguins in the filtered dataset
            return filtered_df().shape[0]

    # Second value box: Displays the average bill length
    with ui.value_box(showcase=icon_svg("ruler-horizontal"),style="background-color: lightblue; color: darkblue;"):
        "Average bill length"

        @render.text
        def bill_length():
            # Calculate and return the mean bill length, rounded to 1 decimal place
            return f"{filtered_df()['bill_length_mm'].mean():.1f} mm"

    # Third value box: Displays the average bill depth
    with ui.value_box(showcase=icon_svg("ruler-vertical"),style="background-color: lightblue; color: darkblue;"):
        "Average bill depth"

        @render.text
        def bill_depth():
            # Calculate and return the mean bill depth, rounded to 1 decimal place
            return f"{filtered_df()['bill_depth_mm'].mean():.1f} mm"
        


# Layout for the main content, including plots and data tables
with ui.layout_columns():
    # First card: Scatterplot of bill length vs. bill depth
    with ui.card(full_screen=True,):
        ui.card_header("Bill length and depth")  # Header for the card

        @render.plot
        def length_depth():
            # Create a scatterplot showing the relationship between bill length and depth
            return sns.scatterplot(
                data=filtered_df(),
                x="bill_length_mm",
                y="bill_depth_mm",
                hue="species",  # Color points by species,
                palette="pastel"
                
            )

    # Second card: Data table with penguin information
    with ui.card(full_screen=True):
        ui.card_header("Penguin Data")  # Header for the card

        @render.data_frame
        def summary_statistics():
            # Define the columns to display in the data table
            cols = [
                "species",
                "island",
                "bill_length_mm",
                "bill_depth_mm",
                "body_mass_g",
            ]
            # Render a data grid with filterable columns
            return render.DataGrid(filtered_df()[cols], filters=True)

# CSS can be included for additional styling, if needed (uncomment the next line to use custom styles)
# ui.include_css("styles.css")

# Reactive function to filter the dataset based on user inputs
@reactive.calc
def filtered_df():
    # Filter by species selected in the checkbox group
    filt_df = df[df["species"].isin(input.species())]
    # Further filter by body mass using the slider input
    filt_df = filt_df.loc[filt_df["body_mass_g"] < input.mass()]
    return filt_df
