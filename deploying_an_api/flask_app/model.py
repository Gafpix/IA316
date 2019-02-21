from tensorflow.keras.layers import Input, Embedding, Flatten, Dot
from tensorflow.keras.models import Model, load_model
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow import get_default_graph

class ModelAPI:
    def __init__(self):
        self.graph = get_default_graph()

    def train(self, nb_users, nb_items, users, items, ratings):
        with self.graph.as_default():
            user_id_input = Input(shape=[1],name='user')
            item_id_input = Input(shape=[1], name='item')

            embedding_size = 5
            user_embedding = Embedding(output_dim=embedding_size, input_dim=nb_users + 1,
                                    input_length=1, name='user_embedding')(user_id_input)

            item_embedding = Embedding(output_dim=embedding_size, input_dim=nb_items + 1,
                                    input_length=1, name='item_embedding')(item_id_input)

            user_vecs = Flatten()(user_embedding)
            item_vecs = Flatten()(item_embedding)

            y = Dot(axes=1)([user_vecs, item_vecs])

            self.model = Model(inputs=[user_id_input, item_id_input], outputs=y)
            self.model.compile(optimizer='adam', loss='MSE')
            early_stopping = EarlyStopping(monitor='val_loss', patience=2)
            self.model.fit([users, items], ratings,
                                batch_size=64, epochs=20, validation_split=0.1,
                                shuffle=True, callbacks=[early_stopping])

    def predict(self, user, item):
        with self.graph.as_default():
            return self.model.predict([[user], [item]])[0,0]
