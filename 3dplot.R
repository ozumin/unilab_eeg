library(plotly)
library(shiny)

merge_data <- function(dat, num){
    filename <- commandArgs(trailingOnly = T)[num]

    data <- read.csv(paste(filename, "result.csv", sep=""))

    alpha <- t(as.matrix(data[9,-1]))
    colnames(alpha) <- NULL
    beta <- t(as.matrix(data[10,-1]))
    colnames(beta) <- NULL
    gamma <- t(as.matrix(data[11,-1]))
    colnames(gamma) <- NULL

    dat <- rbind(dat, data.frame(alpha, beta, gamma, person=filename))

    return(dat)
}

dat <- c()
n <- commandArgs(trailingOnly = T)[1]
for(i in 1:n){
    dat <- merge_data(dat, i+1)
    print(dat)
}
print(dat)

ui <- fluidPage(
    plotlyOutput("plot", width="100%", height="700px")
)

server <- function(input, output, session){
    output$plot <- renderPlotly({
        plot_ly(dat, x=~alpha, y=~beta, color=~person) %>%
#        plot_ly(dat, x=~alpha, y=~beta, z=~gamma, color=~person) %>%
            add_markers()
    })
}

shinyApp(ui = ui, server = server)
