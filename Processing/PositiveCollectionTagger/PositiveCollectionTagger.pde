import java.io.File;

String IMG_DIR = "positive-clean-00";
ArrayList<String> imgFiles;
int currentFile;
String outputBuffer;
PImage currentImg;
PVector[] selectedRegion;
PVector lastMousePressed;
boolean moveSelectedRegion;

void setup() {
  size(1024, 683);

  // populate
  imgFiles = new ArrayList<String>();
  File f = new File(dataPath(IMG_DIR));
  File[] fs = f.listFiles();
  for (int i=0; i<fs.length; i++) {
    if (fs[i].isFile() && (fs[i].getName().endsWith(".JPG") || fs[i].getName().endsWith(".jpg"))) {
      imgFiles.add(IMG_DIR+"/"+fs[i].getName());
    }
  }

  selectedRegion = new PVector[2];
  selectedRegion[0] = new PVector();
  selectedRegion[1] = new PVector();
  lastMousePressed = new PVector();
  moveSelectedRegion = false;

  currentFile = 0;
  outputBuffer = "";
  currentImg = loadImage(imgFiles.get(currentFile));
  initialGuess();
}

void draw() {
  background(0);
  if (currentFile < imgFiles.size()) {
    image(currentImg, 0, 0);
    stroke(0);
    fill(255, 100, 100, 100);
    rect(selectedRegion[0].x, selectedRegion[0].y, selectedRegion[1].x-selectedRegion[0].x, selectedRegion[1].y-selectedRegion[0].y);
  }
  else {
    // some text about saving
  }
}

void initialGuess() {
  currentImg.loadPixels();
  selectedRegion[0].set(currentImg.width,currentImg.height);
  selectedRegion[1].set(0, 0);

  for (int y=0; y<currentImg.height; y++) {
    for (int x=0; x<currentImg.width; x++) {
      color c = currentImg.pixels[y*currentImg.width+x];
      if (((c>>16&0xff) < 250) && ((c>>8&0xff) < 250) && ((c>>0&0xff) < 250)) {
        selectedRegion[0].x = min(selectedRegion[0].x, x);
        selectedRegion[0].y = min(selectedRegion[0].y, y);
        selectedRegion[1].x = max(selectedRegion[1].x, x);
        selectedRegion[1].y = max(selectedRegion[1].y, y);
      }
    }
  }
}

void mousePressed() {
  lastMousePressed.set(mouseX, mouseY);
  moveSelectedRegion = (lastMousePressed.x > selectedRegion[0].x) &&
    (lastMousePressed.x < selectedRegion[1].x) &&
    (lastMousePressed.y > selectedRegion[0].y) &&
    (lastMousePressed.y < selectedRegion[1].y);

  if (!moveSelectedRegion) {
    selectedRegion[0].set(mouseX, mouseY);
  }
}

void mouseDragged() {
  if (!moveSelectedRegion) {
    selectedRegion[1].set(mouseX, mouseY);
  }
  else {
    selectedRegion[0].x += mouseX-pmouseX;
    selectedRegion[0].y += mouseY-pmouseY;
    selectedRegion[1].x += mouseX-pmouseX;
    selectedRegion[1].y += mouseY-pmouseY;
  }
}

void mouseReleased() {
  if (!moveSelectedRegion) {
    selectedRegion[1].set(mouseX, mouseY);
    if (selectedRegion[1].x < selectedRegion[0].x) {
      selectedRegion[1].x = selectedRegion[0].x;
      selectedRegion[0].x = mouseX;
    }
    if (selectedRegion[1].y < selectedRegion[0].y) {
      selectedRegion[1].y = selectedRegion[0].y;
      selectedRegion[0].y = mouseY;
    }
  }
  moveSelectedRegion = false;
}

void keyPressed() {
  if ((key == ' ') && currentFile < imgFiles.size()) {
    outputBuffer += imgFiles.get(currentFile);
    outputBuffer += " 1 ";
    outputBuffer += (int)selectedRegion[0].x+" "+(int)selectedRegion[0].y+" ";
    outputBuffer += (int)(selectedRegion[1].x-selectedRegion[0].x)+" "+(int)(selectedRegion[1].y-selectedRegion[0].y);
    outputBuffer += "\n";
    currentImg = loadImage(imgFiles.get((currentFile+1)%imgFiles.size()));
    initialGuess();
    currentFile++;
  }
  if ((key == 's') && (currentFile == imgFiles.size())) {
    // save string to file
  }
}

