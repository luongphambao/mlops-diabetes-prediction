export MLFLOW_TRACKING_URI=http://localhost:5000
python3 src/train.py --model_name lightgbm
python3 src/train.py --model_name ada_boost
python3 src/train.py --model_name xgb
python3 src/train.py --model_name random_forest
python3 src/train.py --model_name decision_tree
python3 src/train.py --model_name knn
python3 src/train.py --model_name logistic_regression
python3 src/train.py --model_name svm
python3 src/train.py --model_name mlp
python3 src/train.py --model_name naive_bayes
