import Fuse, { IFuseOptions, FuseOptionKey } from 'fuse.js';

interface SearchUtilsOptions<T> {
  keys: FuseOptionKey<T>[];
  threshold?: number;
}

export class SearchUtils<T> {
  private fuse: Fuse<T>;
  private items: T[];

  constructor(items: T[], options: SearchUtilsOptions<T>) {
    const fuseOptions: IFuseOptions<T> = {
      keys: options.keys,
      includeScore: true,
      threshold: options.threshold || 0.3
    };

    this.fuse = new Fuse(items, fuseOptions);
    this.items = items;
  }

  public getAllItems(): T[] {
    return this.items;
  }

  public searchItems(pattern: string): T[] {
    if (!pattern.trim()) return this.getAllItems();
    return this.fuse.search(pattern).map(result => result.item);
  }
}
