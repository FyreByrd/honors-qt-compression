#include "CImg.h"
#define cimg_use_png

using namespace cimg_library;

int main() {
	CImg<unsigned char> image("test_images/splotches.png");
	CImgDisplay main_disp(image, "Image view");

    while (!main_disp.is_closed()) {
        //main_disp.wait();
    }

	return 0;
}
