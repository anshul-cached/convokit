	

def predict(model,parsed_vec,ERROR_THRESHOLD,classes):

	results=model.predict([parsed_vec])[0]
	print (results)
	results = [[i,r] for i,r in enumerate(results) if r>ERROR_THRESHOLD]
	results.sort(key=lambda x: x[1], reverse=True)
	print (results)
	return_list = []
	for r in results:
		return_list.append((classes[r[0]], r[1]))

	return return_list