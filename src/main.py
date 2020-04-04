from dataset import KnowledgeGraph
from model import TransE

import tensorflow as tf
import argparse


def main():
    parser = argparse.ArgumentParser(description='TransE')
    parser.add_argument('--data_dir', type=str, default='../data/')
    parser.add_argument('--embedding_dim', type=int, default=200)
    parser.add_argument('--margin_value', type=float, default=1.0)
    parser.add_argument('--score_func', type=str, default='L1')
    parser.add_argument('--batch_size', type=int, default=4800)
    parser.add_argument('--learning_rate', type=float, default=0.001)
    parser.add_argument('--n_generator', type=int, default=24)
    parser.add_argument('--n_rank_calculator', type=int, default=24)
    parser.add_argument('--ckpt_dir', type=str, default='../ckpt/')
    parser.add_argument('--summary_dir', type=str, default='../summary/')
    parser.add_argument('--max_epoch', type=int, default=500)
    parser.add_argument('--eval_freq', type=int, default=10)
    args = parser.parse_args()
    print(args)
    '''
    传递参数
    Namespace(
        batch_size=4800, 
        ckpt_dir='../ckpt/', 
        data_dir='../data/FB15k/', 
        embedding_dim=200, 
        eval_freq=10, learning_rate=0.001, 
        margin_value=1.0, 
        max_epoch=500, 
        n_generator=24, 
        n_rank_calculator=24, 
        score_func='L1', 
        //summary_dir='../summary/')
    '''
    kg = KnowledgeGraph(data_dir=args.data_dir)#create graph
    kge_model = TransE(
        kg=kg,
        embedding_dim=args.embedding_dim,
        margin_value=args.margin_value,
        score_func=args.score_func,
        batch_size=args.batch_size,
        learning_rate=args.learning_rate,
        n_generator=args.n_generator,
        n_rank_calculator=args.n_rank_calculator
        )#init embd...
    gpu_config = tf.GPUOptions(allow_growth=True)
    '''
    tf.GPUOptions:可以作为设置tf.ConfigProto时的一个参数选项，一般用于限制GPU资源的使用
    allow_growth=True:动态申请现显存
    '''
    sess_config = tf.ConfigProto(gpu_options=gpu_config)
    '''
    tf.ConfigProto:
    创建session的时候，用来对session进行参数配置
    '''
    with tf.Session(config = sess_config) as sess:
        '''
        Session 是 Tensorflow 为了控制,和输出文件的执行的语句. 运行 session.run() 可以获得你要得知的运算结果
        '''
        print('-----Initializing tf graph-----')
        tf.global_variables_initializer().run()#就是 run了 所有global Variable 的 assign op，这就是初始化参数的本来面目。
        print('-----Initialization accomplished-----')
        kge_model.check_norm(session=sess)
        summary_writer = tf.summary.FileWriter(logdir=args.summary_dir, graph=sess.graph)
        # print(type(sess.graph))
        # print(type(summary_writer))
        '''
        logdir: event file
        graph: the graph which needs to be record
        '''
        # for epoch in range(args.max_epoch):
        #     '''
        #     max_epoch: 训练轮数
        #     '''
        #     print('=' * 30 + '[EPOCH {}]'.format(epoch) + '=' * 30)
        #     kge_model.launch_training(session=sess, summary_writer=summary_writer)
        #     if (epoch + 1) % args.eval_freq == 0:#每10轮评估一下
        #         kge_model.launch_evaluation(session=sess)


if __name__ == '__main__':
    main()
