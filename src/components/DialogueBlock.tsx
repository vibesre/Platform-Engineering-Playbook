import React from 'react';
import styles from './DialogueBlock.module.css';

interface DialogueBlockProps {
  speaker: string;
  speakerName: string;
  text: string;
}

export default function DialogueBlock({ speaker, speakerName, text }: DialogueBlockProps): JSX.Element {
  const isJordan = speaker === 'Speaker 1';

  return (
    <div className={`${styles.dialogueBlock} ${isJordan ? styles.jordan : styles.alex}`}>
      <div className={styles.speaker}>
        <div className={styles.avatar}>{speakerName.charAt(0)}</div>
        <span className={styles.speakerName}>{speakerName}</span>
      </div>
      <div className={styles.text}>{text}</div>
    </div>
  );
}
