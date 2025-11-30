# R script to create heatmaps from coalescence data
library(ggplot2)
library(dplyr)

# Load data
data <- read.csv("coalescence_data_all.csv")

# Create heatmap plots for each interaction strength
create_heatmap <- function(u_val) {
  subset_data <- data[data$interaction_strength == u_val, ]
  
  ggplot(subset_data, aes(x = u_coordinate, y = v_coordinate)) +
    stat_density_2d_filled(alpha = 0.8) +
    geom_abline(intercept = 0, slope = 1, linetype = "dashed", alpha = 0.5) +
    xlim(0, 1) + ylim(0, 1) +
    coord_fixed() +
    labs(title = paste("Coalescence Outcomes (u =", u_val, ")"),
         x = "u (contribution from community 1)",
         y = "v (contribution from community 2)") +
    theme_minimal()
}

# Create plots
p1 <- create_heatmap("0.3")
p2 <- create_heatmap("0.5")
p3 <- create_heatmap("0.8")

# Save plots
ggsave("heatmap_u0.3.png", p1, width = 8, height = 6, dpi = 300)
ggsave("heatmap_u0.5.png", p2, width = 8, height = 6, dpi = 300)
ggsave("heatmap_u0.8.png", p3, width = 8, height = 6, dpi = 300)

print("Heatmaps saved as PNG files")
