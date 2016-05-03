package GUI;

import javafx.fxml.FXML;
import javafx.scene.control.Button;
import javafx.scene.control.ProgressBar;


public class WindowController {
    @FXML
    private Button startButton;
    @FXML
    private Button downloadButton;
    @FXML
    private Button imageButton;
    @FXML
    private ProgressBar lapProgress;
    @FXML
    private ProgressBar downloadProgress;


    @FXML
    private void initiateLap(){
        System.out.println("Initiating lap");
    }

    @FXML
    private void initiateDownload(){
        System.out.println("Initiating download");
    }
    @FXML
    private void takeImage(){
        System.out.println("Picture taken");
    }

}
