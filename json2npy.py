def json2npy():
    data_root = OUT_DATA_DIR

    character_names = os.listdir(data_root)
    print(character_names)

    total_num = 0
    for char in character_names:
        char_dir = os.path.join(data_root, char)
        animation_names = os.listdir(char_dir)

        for anim in animation_names:
            joint_dir = os.path.join(char_dir, anim, 'jointsDict')

            nr_files = len(os.listdir(joint_dir))
            motion = []
            for i in range(0, nr_files):
                with open(os.path.join(joint_dir, '%04d_keypoints.json' % i)) as f:
                    info = json.load(f)
                    joint = np.array(info['pose_keypoints_3d']).reshape((-1, 3))
                motion.append(joint[:15, :])

            motion = np.stack(motion, axis=2)
            save_path = os.path.join(char_dir, anim, '{}.npy'.format(anim))
            print(save_path)
            np.save(save_path, motion)


if __name__ == '__main__':
    main()
    # further convert json to npy
    json2npy()