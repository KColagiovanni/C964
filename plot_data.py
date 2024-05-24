import matplotlib.pyplot as plt
from PyQt5.QtWidgets import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from process_and_train_data import ProcessAndTrainData
import numpy as np


class PlotData(QWidget):

    def __init__(self, data_frame):
        super().__init__()

        # Define the data frame
        self.data_frame = data_frame

        # Define dimension variables
        self.left = 0
        self.top = 400
        self.width = 1000
        self.height = 650
        canvas_width = 900
        canvas_height = 500
        self.graph_button_height = 40

        # Define color variables
        self.bg_color = 'lightgray'
        self.max_bar_color = 'red'
        self.pos_bar_color = 'orange'
        self.neg_bar_color = 'lightgreen'
        self.min_bar_color = 'lightblue'

        # Data frame columns
        self.column_names = [
            'Pregnancies',  # Number of pregnancies
            'Glucose',  # Plasma glucose concentration (2 hours in an oral glucose tolerance test)(mg/dl)
            'BloodPressure',  # Diastolic blood pressure (mm Hg)
            'SkinThickness',  # Triceps skin fold thickness (mm)
            'Insulin',  # 2-Hour serum insulin (mu U/ml)
            'BMI',  # Body mass index (weight in kg/(height in m)^2)
            'DiabetesPedigreeFunction',  # Likelihood of having diabetes based on family history
            'Age'  # Age in Years
        ]

        # Define the figure
        self.figure = plt.figure(figsize=(canvas_width, canvas_height), layout='constrained')

        # Define the canvas widget that displays the 'figure'
        self.canvas = FigureCanvas(self.figure)

        # Define the window buttons
        self.bar_graph_button = QPushButton('Show Bar Graph')
        self.scatter_plot_button = QPushButton('Show Scatter Plot')
        self.new_plot_button = QPushButton('Show Histogram Graph')
        self.close_plot_window_button = QPushButton('Close Window')

        # Define a checkbox and label to show or hide zero values in plots
        self.hide_zero_values = QCheckBox('Hide data with a value of "0"')

        # Defining a label for the dropdown(ComboBox)
        self.select_a_plot_label = QLabel('Select Data to Plot:')

        # Define a horizontal line to be used as a seperator
        self.horizontal_line = QLabel()

        # Define progress bar
        self.progress_bar = QProgressBar(self)

        # Dropdown menu to select which scatter plot tp display
        self.select_plot_dropdown = QComboBox(self)

        # Call the method to initialize the define widgets ad create layouts
        self.initialize_user_interface()

    def initialize_user_interface(self):

        # Define the window title
        self.setWindowTitle('Graph Data')

        # Define the prediction window geometry
        self.setGeometry(self.left, self.top, self.width, self.height)

        # Call the method to modify (define functionality) the widgets
        self.modify_widgets()

        # Vertical layout (Widgets are stacked vertically)
        plot_window_layout = QVBoxLayout()

        # Horizontal layout (Widgets are stacked horizontally)
        plot_selection_layout = QHBoxLayout()

        # Define group box
        plot_groupbox = QGroupBox()
        plot_groupbox.setStyleSheet(f'background-color: {self.bg_color}')

        # Adding widgets to the plot selection horizontal layout
        plot_selection_layout.addWidget(plot_groupbox)

        # Adding and defining layouts
        scatter_plot_groupbox_layout = QGridLayout()
        plot_groupbox.setLayout(scatter_plot_groupbox_layout)

        # Adding the scatter plot widgets to the groupbox layout and defining their grid position
        scatter_plot_groupbox_layout.addWidget(self.select_a_plot_label, 0, 0)
        scatter_plot_groupbox_layout.addWidget(self.select_plot_dropdown, 1, 0)
        scatter_plot_groupbox_layout.addWidget(self.hide_zero_values, 1, 2)
        scatter_plot_groupbox_layout.addWidget(self.horizontal_line, 2, 0, 1, 3)
        scatter_plot_groupbox_layout.addWidget(self.bar_graph_button, 3, 0)
        scatter_plot_groupbox_layout.addWidget(self.scatter_plot_button, 3, 1)
        scatter_plot_groupbox_layout.addWidget(self.new_plot_button, 3, 2)
        scatter_plot_groupbox_layout.addWidget(self.close_plot_window_button, 4, 0, 1, 3)

        # Adding widgets to the plot window vertical layout
        plot_window_layout.addWidget(self.canvas)
        plot_window_layout.addWidget(self.progress_bar)
        plot_window_layout.addLayout(plot_selection_layout)

        # Setting the layout
        self.setLayout(plot_window_layout)

    def modify_widgets(self):

        # Defining the methods to be called
        self.bar_graph_button.clicked.connect(self.bar_graph)
        self.scatter_plot_button.clicked.connect(self.scatter_plot)
        self.new_plot_button.clicked.connect(self.histogram_plot)
        self.close_plot_window_button.clicked.connect(self.close_plot_window)
        self.select_plot_dropdown.currentIndexChanged.connect(self.get_changed_status_from_dropdown)

        # Adding items to the dropdown(ComboBox)
        self.select_plot_dropdown.addItems(self.column_names)

        # Set the checkbox to be checked by default
        self.hide_zero_values.setChecked(True)

        # Set the horizontal line
        self.horizontal_line.setFrameStyle(QFrame.HLine)

        # Setting button height
        self.bar_graph_button.setFixedHeight(self.graph_button_height)
        self.scatter_plot_button.setFixedHeight(self.graph_button_height)
        self.new_plot_button.setFixedHeight(self.graph_button_height)
        self.close_plot_window_button.setFixedHeight(self.graph_button_height)

    def get_changed_status_from_dropdown(self):

        # If the pregnancies column is picked, hide the "Hide Zero Values" checkbox, otherwise show it.
        if self.select_plot_dropdown.currentIndex() == 0:
            self.hide_zero_values.setHidden(True)
        else:
            self.hide_zero_values.setHidden(False)

    def bar_graph(self):

        # Define an instance of the process object
        ptd = ProcessAndTrainData(self.data_frame)

        # Clearing figure so current one can be displayed
        self.figure.clear()

        # Add a subplot to the figure
        ax = self.figure.add_subplot(1, 1, 1)

        # Get the index of the current select plot dropdown selection
        column_index = self.select_plot_dropdown.currentIndex()

        # Get the min and max values from the dataframe, and also the average values from the negative only and positive
        # only datasets of the selected column
        X_max = ptd.X[self.column_names[column_index]].max()
        X_min = ptd.X[self.column_names[column_index]].min()
        neg_avg = ptd.neg[self.column_names[column_index]].mean()
        pos_avg = ptd.pos[self.column_names[column_index]].mean()

        # If the selected column is "BMI", round the result 1 decimal place after the decimal
        if self.column_names[column_index] == 'BMI':
            X_max = round(X_max, 1)
            pos_avg = round(pos_avg, 1)
            neg_avg = round(neg_avg, 1)
            X_min = round(X_min, 1)

        # If the selected column is "DiabetesPedigreeFunction", round the result 2 decimal places after the decimal
        elif self.column_names[column_index] == 'DiabetesPedigreeFunction':
            X_max = round(X_max, 2)
            pos_avg = round(pos_avg, 2)
            neg_avg = round(neg_avg, 2)
            X_min = round(X_min, 2)

        # Else convert to integer
        else:
            X_max = int(X_max)
            pos_avg = int(pos_avg)
            neg_avg = int(neg_avg)
            X_min = int(X_min)

        # Plot max data
        ax.bar(1, X_max, color=self.max_bar_color, width=1)
        ax.text(1, X_max / 2, str(X_max), ha='center')

        # Plot avg data from the positive dataset
        ax.bar(2, pos_avg, color=self.pos_bar_color, width=1)
        ax.text(2, pos_avg / 2, str(pos_avg), ha='center')

        # Plot avg data from the negative dataset
        ax.bar(3, neg_avg, color=self.neg_bar_color, width=1)
        ax.text(3, neg_avg / 2, str(neg_avg), ha='center')

        # Plot min data
        ax.bar(4, X_min, color=self.min_bar_color, width=1)
        if X_min < 0.1:
            ax.text(4, X_min, str(X_min), ha='center')
        else:
            ax.text(4, X_min / 2, str(X_min), ha='center')

        # Define the plot title, and center it and also remove the x-axis tick marks
        ax.set_title(self.column_names[column_index], loc='center')
        ax.tick_params(bottom=False, labelbottom=False)

        # Display the legend
        self.figure.legend(['Max Values', 'Has Diabetes Avg', 'Doesn\'t Have Diabetes Avg', 'Min Values'])

        # Draw the graph on the canvas
        self.canvas.draw()

    def scatter_plot(self):

        # Define local variables
        zero_count = 0
        percent_dropped = 0

        # Clearing old figure
        self.figure.clear()

        # Add a subplot to the figure
        ax = self.figure.add_subplot(1, 1, 1)

        # Get the index of the current select plot dropdown selection
        column_index = self.select_plot_dropdown.currentIndex()

        min_data_frame_value = self.data_frame[self.column_names[column_index]].max()

        print(f'\n\nStarting to process the {self.column_names[column_index]} column')

        # Filter and plot each data point in the column.
        for data_point in range(len(self.data_frame.to_numpy())):

            # Progress bar progress
            progress_status = int(((data_point + 1) / self.data_frame.shape[0]) * 100)
            if progress_status <= 100:
                print(
                    f'Scatter Plot Loading Progress: {int(((data_point + 1) / len(self.data_frame.to_numpy())) * 100)}%'
                )
                self.progress_bar.setValue(progress_status)
                self.progress_bar.setFormat(f'Processing Data: {progress_status + 1}%')

            # Plot the data points in green when the patient doesn't have diabetes and red then they do.
            if self.data_frame.to_numpy()[data_point][8] == 0:  # Does not have diabetes.
                color = 'green'
            else:  # Has diabetes.
                color = 'red'

            # If any column, except the "Pregnancies" column
            if self.column_names[column_index] != 'Pregnancies':

                # If the "Hide Zero Values" check box is checked
                if self.hide_zero_values.isChecked():

                    # If the datapoint is 0, ignor it, otherwise plot it
                    if self.data_frame.to_numpy()[data_point][column_index] > 0:

                        # Determining the min value for the data frame
                        if self.data_frame.to_numpy()[data_point][column_index] < min_data_frame_value:
                            min_data_frame_value = self.data_frame.to_numpy()[data_point][column_index]
                        else:
                            self.data_frame.to_numpy()[data_point][column_index] = min_data_frame_value

                        # Calculating the steps to the x-axis ticks
                        if self.column_names[column_index] == 'BMI':
                            steps = round(
                                (self.data_frame[self.column_names[column_index]].max() - min_data_frame_value) / 10, 1)
                        elif self.column_names[column_index] == 'DiabetesPedigreeFunction':
                            steps = round(
                                (self.data_frame[self.column_names[column_index]].max() - min_data_frame_value) / 10, 2)
                        else:
                            steps = (self.data_frame[
                                         self.column_names[column_index]].max() - min_data_frame_value) // 10

                        # Plot the scatter point
                        ax.scatter(self.data_frame.to_numpy()[data_point][column_index], data_point, color=color)

                        # Set the a-axis ticks, start with the min value and end at the max value, using the step size
                        # defined above.
                        ax.xaxis.set_ticks(np.arange(
                            min_data_frame_value,
                            self.data_frame[self.column_names[column_index]].max(),
                            steps
                        ))

                        zero_count += 1

                # If the "Hide Zero Values" check box is not checked
                else:

                    # Determining the min value for the data frame
                    if self.data_frame.to_numpy()[data_point][column_index] < min_data_frame_value:
                        min_data_frame_value = self.data_frame.to_numpy()[data_point][column_index]
                    else:
                        self.data_frame.to_numpy()[data_point][column_index] = min_data_frame_value

                    # Calculating the steps to the x-axis ticks
                    if self.column_names[column_index] == 'BMI':
                        steps = round(
                            (self.data_frame[self.column_names[column_index]].max() - min_data_frame_value) / 10, 1
                        )
                    elif self.column_names[column_index] == 'DiabetesPedigreeFunction':
                        steps = round(
                            (self.data_frame[self.column_names[column_index]].max() - min_data_frame_value) / 10, 2
                        )
                    else:
                        steps = (self.data_frame[self.column_names[column_index]].max() - min_data_frame_value) // 10

                    # Plot the scatter point
                    ax.scatter(self.data_frame.to_numpy()[data_point][column_index], data_point, color=color)

                    # Set the a-axis ticks, start with the min value and end at the max value, using the step size
                    # defined above.
                    ax.xaxis.set_ticks(
                        np.arange(min_data_frame_value, self.data_frame[self.column_names[column_index]].max(), steps)
                    )

                    zero_count = self.data_frame.shape[0]

                # Calculate the number of data points have been ignored, or dropped
                percent_dropped = round((self.data_frame.shape[0] - zero_count) / self.data_frame.shape[0] * 100, 1)

            # Plot all pregnancy data.
            if self.column_names[column_index] == 'Pregnancies':

                # Plot the scatter point
                ax.scatter(self.data_frame.to_numpy()[data_point][column_index], data_point, color=color)

                # Set the a-axis ticks, start with the min value and end at the max value.
                ax.xaxis.set_ticks(np.arange(0, 18, 1))

                zero_count = self.data_frame.shape[0]

                percent_dropped = 0

        print(f'Showing the {self.column_names[column_index]} plot. ({self.data_frame.shape[0] - zero_count}'
              f' zero points have been dropped({percent_dropped}%))')

        # Defining the plot legend
        ax.legend(['Has diabetes', 'Does not have diabetes'], loc='upper right')

        # Define plot title
        ax.set_title(self.column_names[column_index])

        # Remove y ticks
        ax.tick_params(left=False, labelleft=False)  # Remove y-axis tick marks and labels

        # Display the plot
        self.canvas.draw()

        # Reset the progres bar
        self.progress_bar.reset()

    def histogram_plot(self):

        # Clearing old figure
        self.figure.clear()

        # Add a subplot to the figure
        ax = self.figure.add_subplot(1, 1, 1)

        # Get the index of the current select plot dropdown selection
        column_index = self.select_plot_dropdown.currentIndex()

        print(f'\n\nStarting to process the {self.column_names[column_index]} column')

        # Define the plot title
        ax.set_title(self.column_names[column_index])

        # Drop all zero values in every column, except for the pregnancy column. Also define # of bins and x ticks.
        if self.column_names[column_index] == 'Pregnancies':
            bins = 17
            no_zeros_data_frame = self.data_frame[self.column_names[column_index]]
            ax.xaxis.set_ticks(np.arange(0, bins, 1))

        elif self.hide_zero_values.isChecked():
            bins = 20
            no_zeros_data_frame = self.data_frame[
                self.column_names[column_index]][self.data_frame[self.column_names[column_index]] != 0]

        else:
            bins = 20
            no_zeros_data_frame = self.data_frame[self.column_names[column_index]]

        # Define the step number for the histogram plot
        if self.column_names[column_index] == 'BMI':
            steps = round(((no_zeros_data_frame.max() - no_zeros_data_frame.min()) / 10), 1)
        elif self.column_names[column_index] == 'DiabetesPedigreeFunction':
            steps = round(((no_zeros_data_frame.max() - no_zeros_data_frame.min()) / 10), 2)
        else:
            steps = (no_zeros_data_frame.max() - no_zeros_data_frame.min()) // 10

        # Plot the Histogram
        ax.hist(no_zeros_data_frame.to_numpy(), bins=bins)

        # Set the a-axis ticks, start with the min value and end at the max value, using the step size
        # defined above.
        ax.xaxis.set_ticks(np.arange(round(no_zeros_data_frame.min(), 2), no_zeros_data_frame.max(), steps))

        # Display the histogram
        self.canvas.draw()

    def close_plot_window(self):

        print('Closing the Graph Window')

        # Close the graph window
        self.close()
