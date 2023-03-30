#include <iostream>

int main() {
	int result = 0;
	int oneCounter = 0;
	std::string roman;
	std::cin >> roman;
	for (int i = 0; i < roman.size(); i++) {
		if (roman.at(i) == 'I')
			oneCounter++;
		else if (roman.at(i) == 'V') {
			if (oneCounter > 2) {
				result += 3;
				oneCounter -= 2;
				result += oneCounter;
			}
			else
				result += (5 - oneCounter);
			oneCounter = 0;
		}
		else {
			if (oneCounter > 2) {
				result += 8;
				oneCounter -= 2;
				result += oneCounter;
			}
			else
				result += (10 - oneCounter);
			oneCounter = 0;
		}
	}
	result += oneCounter;
	std::cout << result << std::endl;
}