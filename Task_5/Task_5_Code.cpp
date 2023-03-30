#include <iostream>
#include <vector>


int kmp(std::string x) {
	int maxVal = 0;
	int tempIdx = 0;
	std::vector<int> failure;
	failure.assign(x.size(), 0);
	for (int i = 1; i < x.size(); i++) {
		if (x[failure[i - 1]] == x[i])
			failure[i] = failure[i - 1] + 1;
		else {
			if (failure[i - 1] - 1 < 0)
				continue;
			tempIdx = failure[failure[i - 1] - 1];
			while (1) {
				if (x[tempIdx] == x[i]) {
					failure[i] = tempIdx + 1;
					break;
				}
				else if (tempIdx == 0)
					break;
				else {
					tempIdx = failure[tempIdx - 1];
					if (tempIdx < 0)
						break;
				}
			}
		}
		if (failure[i] > maxVal)
			maxVal = failure[i];
	}
	return maxVal;
}


int main() {
	int maxLength = 0;
	int result;
	std::string line;
	std::cin >> line;
	for (int i = 0; i < line.size(); i++) {
		std::string subLine = line.substr(i);
		result = kmp(subLine);
		if (result > maxLength)
			maxLength = result;
	}
	std::cout << maxLength << std::endl;
}