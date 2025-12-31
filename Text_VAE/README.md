See on colab: (https://colab.research.google.com/drive/17vrHotYJ0FYI2dUtnA6Ty56Vu5BWS9LH?usp=sharing)

This is a VAE that maps text to a latent space instead of images. Run all the cells. The second cell contains the architecture and training function, while the subsequent cells contain interactive demonstrations where the user can give their own inputs for interpolation.

Text is encoded as a probability distribution in a 200-dimensional latent space by being run through an LSTM, the hidden state of which is fed forward to create a mean and standard distribution for it. The decoder takes a latent vector through a feed-forward network and concatenates it to the input of each step of a decoder LSTM that outputs the text. By interpolating between latent vectors, the text itself is interpolated while still retaining coherency and meaning. There is also a significant amount of word arithmetic possible e.g. red cat + blue dog - blue cat = red dog.

More Info: [https://docs.google.com/document/d/1CzCFt0hM7eb4-oK0jRMwN4QWdBgrSXuS7MwH5ODRWLQ/edit?usp=sharing](url)
