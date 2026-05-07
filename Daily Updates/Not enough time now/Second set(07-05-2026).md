Here's the updated C++ conversion with time and space complexity added to each:


# Backtracking Algorithms in C++

## Subsets
```cpp
vector<vector<int>> subsets(vector<int>& nums) {
    vector<vector<int>> result;
    sort(nums.begin(), nums.end());
    vector<int> temp;
    backtrack(result, temp, nums, 0);
    return result;
}

void backtrack(vector<vector<int>>& result, vector<int>& temp, vector<int>& nums, int start) {
    result.push_back(temp);
    for(int i = start; i < nums.size(); i++) {
        temp.push_back(nums[i]);
        backtrack(result, temp, nums, i + 1);
        temp.pop_back();
    }
}
// Time Complexity: O(n * 2^n) - 2^n subsets, each taking O(n) to copy
// Space Complexity: O(n) - recursion stack depth, plus O(n * 2^n) for output
```

Subsets With Duplicates

```cpp
vector<vector<int>> subsetsWithDup(vector<int>& nums) {
    vector<vector<int>> result;
    sort(nums.begin(), nums.end());
    vector<int> temp;
    backtrack(result, temp, nums, 0);
    return result;
}

void backtrack(vector<vector<int>>& result, vector<int>& temp, vector<int>& nums, int start) {
    result.push_back(temp);
    for(int i = start; i < nums.size(); i++) {
        if(i > start && nums[i] == nums[i-1]) continue;
        temp.push_back(nums[i]);
        backtrack(result, temp, nums, i + 1);
        temp.pop_back();
    }
}
// Time Complexity: O(n * 2^n) - worst case with all distinct elements
// Space Complexity: O(n) - recursion stack depth, plus O(n * 2^n) for output
```

Permutations

```cpp
vector<vector<int>> permute(vector<int>& nums) {
    vector<vector<int>> result;
    vector<int> temp;
    backtrack(result, temp, nums);
    return result;
}

void backtrack(vector<vector<int>>& result, vector<int>& temp, vector<int>& nums) {
    if(temp.size() == nums.size()) {
        result.push_back(temp);
    } else {
        for(int i = 0; i < nums.size(); i++) {
            if(find(temp.begin(), temp.end(), nums[i]) != temp.end()) continue;
            temp.push_back(nums[i]);
            backtrack(result, temp, nums);
            temp.pop_back();
        }
    }
}
// Time Complexity: O(n * n!) - n! permutations, each taking O(n) to copy
// Space Complexity: O(n) - recursion stack depth, plus O(n * n!) for output
```

Permutations Unique

```cpp
vector<vector<int>> permuteUnique(vector<int>& nums) {
    vector<vector<int>> result;
    sort(nums.begin(), nums.end());
    vector<int> temp;
    vector<bool> used(nums.size(), false);
    backtrack(result, temp, nums, used);
    return result;
}

void backtrack(vector<vector<int>>& result, vector<int>& temp, vector<int>& nums, vector<bool>& used) {
    if(temp.size() == nums.size()) {
        result.push_back(temp);
    } else {
        for(int i = 0; i < nums.size(); i++) {
            if(used[i] || i > 0 && nums[i] == nums[i-1] && !used[i-1]) continue;
            used[i] = true;
            temp.push_back(nums[i]);
            backtrack(result, temp, nums, used);
            used[i] = false;
            temp.pop_back();
        }
    }
}
// Time Complexity: O(n * n!) - worst case with all distinct elements
// Space Complexity: O(n) - recursion stack depth plus used array, plus O(n * n!) for output
```

Combination Sum (Unlimited Usage)

```cpp
vector<vector<int>> combinationSum(vector<int>& nums, int target) {
    vector<vector<int>> result;
    sort(nums.begin(), nums.end());
    vector<int> temp;
    backtrack(result, temp, nums, target, 0);
    return result;
}

void backtrack(vector<vector<int>>& result, vector<int>& temp, vector<int>& nums, int remain, int start) {
    if(remain < 0) return;
    else if(remain == 0) result.push_back(temp);
    else {
        for(int i = start; i < nums.size(); i++) {
            temp.push_back(nums[i]);
            backtrack(result, temp, nums, remain - nums[i], i);
            temp.pop_back();
        }
    }
}
// Time Complexity: O(n^(target/min)) - branching factor depends on target value
// Space Complexity: O(target/min) - recursion depth, where min is smallest number in nums
```

Palindrome Partitioning

```cpp
vector<vector<string>> partition(string s) {
    vector<vector<string>> result;
    vector<string> temp;
    backtrack(result, temp, s, 0);
    return result;
}

void backtrack(vector<vector<string>>& result, vector<string>& temp, string& s, int start) {
    if(start == s.length()) {
        result.push_back(temp);
    } else {
        for(int i = start; i < s.length(); i++) {
            if(isPalindrome(s, start, i)) {
                temp.push_back(s.substr(start, i - start + 1));
                backtrack(result, temp, s, i + 1);
                temp.pop_back();
            }
        }
    }
}

bool isPalindrome(string& s, int low, int high) {
    while(low < high) {
        if(s[low++] != s[high--]) return false;
    }
    return true;
}
// Time Complexity: O(n * 2^n) - worst case when all characters are same, 2^n partitions
// Space Complexity: O(n) - recursion stack depth, plus O(n * 2^n) for output
```

Complexity Summary Table

Problem Time Complexity Space Complexity
Subsets O(n * 2^n) O(n * 2^n)
Subsets With Duplicates O(n * 2^n) O(n * 2^n)
Permutations O(n * n!) O(n * n!)
Permutations Unique O(n * n!) O(n * n!)
Combination Sum O(n^(target/min)) O(target/min)
Palindrome Partitioning O(n * 2^n) O(n * 2^n)

Note: Space complexity includes the output storage. For the recursion stack alone, it's O(n) for all algorithms except combination sum where it's O(target/min).